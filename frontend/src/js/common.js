(function(){
  window.$qs = function(name){
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name) || "";
  };

  window.$api = {
    async search(params){
      const base = window.APP_CONFIG.BACKEND_BASE_URL;
      const url = `${base}/search?${$.param(params)}`;
      return $.getJSON(url);
    },
    async bbox(bounds, filters){
      const base = window.APP_CONFIG.BACKEND_BASE_URL;
      const q = $.param({
        minLng: bounds.getWest(),
        minLat: bounds.getSouth(),
        maxLng: bounds.getEast(),
        maxLat: bounds.getNorth(),
        ...filters
      });
      return $.getJSON(`${base}/bbox?${q}`);
    },
    async postKnowledge(obj){
      const base = window.APP_CONFIG.BACKEND_BASE_URL;
      return $.ajax({url: `${base}/post`, method: 'POST', contentType: 'application/json', data: JSON.stringify(obj)});
    },
    async getUploadUrl(filename, contentType){
      const base = window.APP_CONFIG.BACKEND_BASE_URL;
      return $.ajax({url: `${base}/upload-url`, method: 'POST', contentType: 'application/json', data: JSON.stringify({ filename, contentType })});
    }
  };

  window.$ui = {
    itemToCard(item){
      const html = `
      <article class="card-tile" data-geo="${item.GeoLocation}">
        <img src="${item.S3ImageURL}" alt="image" onerror="this.src='https://placehold.co/600x400?text=No+Image'" />
        <div class="tile-body">
          <div class="tile-title">${$('<div>').text(item.Description).html()}</div>
          <div class="tile-meta">${item.City ? item.City+', ' : ''}${item.Country || ''} • ${item.Category || ''} • ${item.KnowledgeType || ''}</div>
          <a class="btn" target="_blank" href="/view.html?${$.param(item)}">Open</a>
        </div>
      </article>`;
      return $(html);
    },
    ensureYear(id){ $(id).text(new Date().getFullYear()); }
  };
})();