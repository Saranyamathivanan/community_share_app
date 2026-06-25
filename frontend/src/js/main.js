(async function() {
  const cfg = window.APP_CONFIG;
  let map;
  let markers = [];
  let initialSearchResults = null;

  // --- API helpers ---
  async function fetchSearch(params) {
    const url = `${cfg.BACKEND_BASE_URL}/search?${$.param(params)}`;
    return $.getJSON(url);
  }

  async function fetchBBox(bounds) {
    const url = `${cfg.BACKEND_BASE_URL}/bbox?${$.param({
      minLng: bounds.getWest(),
      minLat: bounds.getSouth(),
      maxLng: bounds.getEast(),
      maxLat: bounds.getNorth()
    })}`;
    return $.getJSON(url);
  }

  // --- UI: clear markers ---
  function clearPins() {
    markers.forEach(m => m.remove());
    markers = [];
  }

  // --- UI: render pins on map ---
  function renderPins(items) {
    clearPins();
    items.forEach(item => {
      if (!item.GeoLocation) return;
      const [latStr, lngStr] = item.GeoLocation.split(",");
      const lat = parseFloat(latStr), lng = parseFloat(lngStr);
      if (!Number.isFinite(lat) || !Number.isFinite(lng)) return;

      const el = document.createElement("div");
      el.className = "map-pin";
      el.title = item.Description;
      el.addEventListener("click", () => {
        console.log("Pin clicked", item);
        showDetailPopup(item);
      });

      const marker = new maplibregl.Marker(el)
        .setLngLat([lng, lat])
        .addTo(map);
      markers.push(marker);
    });
  }

  // --- UI: render image tiles ---
  function renderTiles(items) {
    let $tiles = $("#tiles");
    if ($tiles.length === 0) {
      // If #tiles doesn't exist, create it and add to layout
      $tiles = $('<div id="tiles"></div>');
      if ($('.layout').length) {
        $('.layout').append($tiles);
      } else {
        $('.container').append($tiles);
      }
    }
    $tiles.empty();
    if (!items.length) {
      $tiles.html("<p>No results found in this area.</p>");
      return;
    }
    items.forEach(item => {
      const html = `
        <div class="tile" tabindex="0" data-item='${item ? JSON.stringify(item).replace(/'/g, "&apos;") : "{}"}'>
          <img src="${item.S3ImageURL}" alt="preview">
          <p>${item.Description}</p>
        </div>
      `;
      $tiles.append(html);
    });

    $(".tile").off("click").on("click", function() {
      const item = $(this).data("item");
      showDetailPopup(item);
    });
    // Optional: allow keyboard accessibility
    $(".tile").off("keydown").on("keydown", function(e) {
      if (e.key === "Enter" || e.key === " ") {
        const item = $(this).data("item");
        showDetailPopup(item);
      }
    });
  }

  // --- Show detail popup ---
  function showDetailPopup(item) {
    // Remove any existing popup
    $("#detail-popup").remove();
    // Build popup HTML
    const popupHtml = `
      <div id="detail-popup" class="detail-popup-overlay">
        <div class="detail-popup-card">
          <button class="detail-popup-close" aria-label="Close">&times;</button>
          ${item.S3ImageURL ? 
            `<img src="${item.S3ImageURL}" alt="Community Knowledge Image">` : 
            `<div class="img-placeholder">No image available</div>`
          }
          <h2>${item.Description}</h2>
          <p>${item.DetailedDescription || ""}</p>
          <div class="meta">
            <p><strong>UserID:</strong> ${item.UserID || ""}</p>
            <p><strong>Country:</strong> ${item.Country || ""}</p>
            <p><strong>City:</strong> ${item.City || ""}</p>
            <p><strong>GeoLocation:</strong> ${item.GeoLocation || ""}</p>
            <p><strong>Category:</strong> ${item.Category || ""}</p>
            <p><strong>Knowledge Type:</strong> ${item.KnowledgeType || ""}</p>
          </div>
        </div>
      </div>
    `;
    $("body").append(popupHtml);

    // Close handlers
    $(".detail-popup-close, #detail-popup").on("click", function(e) {
      if (e.target === this) $("#detail-popup").remove();
    });
    // ESC key closes popup
    $(document).on("keydown.detailPopup", function(e) {
      if (e.key === "Escape") $("#detail-popup").remove();
    });
  }

  // --- Remove popup on close ---
  $(document).on("click", ".detail-popup-close", function() {
    $("#detail-popup").remove();
    $(document).off("keydown.detailPopup");
  });

  // --- Load initial data ---
  async function loadInitial() {
    // Check for searchResults in sessionStorage
    let items = [];
    const stored = sessionStorage.getItem("searchResults");
    if (stored) {
      try {
        items = JSON.parse(stored);
        initialSearchResults = items;
        sessionStorage.removeItem("searchResults");
      } catch (e) {
        items = [];
      }
    } else {
      // Only search if country is present
      var country = $("#f-country").val().trim();
      if (!country) {
        country=cfg.DEFAULT_COUNTRY || "New Zealand";
        $("#f-country").val(country);
        alert(`No country specified. Defaulting to "${country}".`);
      }
      items = await fetchSearch({ country });
    }
    
    // If we have search results, center map on first result
    if (items.length && items[0].GeoLocation) {
      const [latStr, lngStr] = items[0].GeoLocation.split(",");
      const lat = parseFloat(latStr.trim()), lng = parseFloat(lngStr.trim());
      if (Number.isFinite(lat) && Number.isFinite(lng)) {
        map.setCenter([lng, lat]);
        map.setZoom(6);
      }
    }
    const bounds = map.getBounds();
    items = await fetchBBox(bounds).catch(() => []);
    renderTiles(items);
    renderPins(items);
  }

  // --- Refresh on map move ---
  async function refreshOnMove() {
    // If initial search results were just loaded, skip first move event
    if (initialSearchResults) {
      initialSearchResults = null;
      return;
    }
    const bounds = map.getBounds();
    const items = await fetchBBox(bounds).catch(() => []);
    renderTiles(items);
    renderPins(items);
  }

  // --- Handle filter form submission ---
  window.applyFilters = async function() {
    console.log("applyFilters called");
    var country = $("#f-country").val().trim();
    if (!country) {
      alert("Please enter a country to search.");
      $("#f-country").focus();
      return;
    }
    const params = {
      country,
      city: $("#f-city").val().trim(),
      category: $("#f-category").val(),
      type: $("#f-type").val()
    };
    // Remove empty values except country
    Object.keys(params).forEach(k => {
      if (!params[k] && k !== "country") delete params[k];
    });

    const items = await fetchSearch(params);

    // Center map on first result if available
    if (items.length && items[0].GeoLocation) {
      const [latStr, lngStr] = items[0].GeoLocation.split(",");
      const lat = parseFloat(latStr.trim()), lng = parseFloat(lngStr.trim());
      if (Number.isFinite(lat) && Number.isFinite(lng)) {
        map.setCenter([lng, lat]);
        map.setZoom(6);
      }
    }
    const bounds = map.getBounds();
    const bboxItems = await fetchBBox(bounds).catch(() => []);
    renderTiles(bboxItems);
    renderPins(bboxItems);
  };

  // --- Init AWS Location Map (using map.html pattern) ---
  async function initMap() {
    const identityPoolId = cfg.MAP_IDENTITY_POOL_ID;
    const mapName = cfg.MAP_NAME;
    const region = cfg.AWS_REGION;

    const authHelper = await amazonLocationAuthHelper.withIdentityPoolId(identityPoolId);

    // Ensure .layout exists and has map and tiles containers
    let $layout = $(".layout");
    if ($layout.length === 0) {
      $layout = $('<section class="layout"></section>');
      $(".container").prepend($layout);
    }
    if ($("#map").length === 0) {
      $layout.prepend('<div id="map"></div>');
    }
    if ($("#tiles").length === 0) {
      $layout.append('<div id="tiles"></div>');
    }

    map = new maplibregl.Map({
      container: "map",
      center: [174.7633, -36.8485], // Auckland default
      zoom: 5,
      style: `https://maps.geo.${region}.amazonaws.com/maps/v0/maps/${mapName}/style-descriptor`,
      ...authHelper.getMapAuthenticationOptions(),
    });

    map.addControl(new maplibregl.NavigationControl(), "top-right");

    map.on("load", loadInitial);
    map.on("moveend", refreshOnMove);
  }

  // --- Start ---
  initMap();
})();


