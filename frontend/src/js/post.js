(async function(){
  if(!document.getElementById('post-form')) return; // only run on post.html
  $ui.ensureYear('#year3');

  const cfg = window.APP_CONFIG;

  // ==== 1) Configure Amplify Auth for Hosted UI (Implicit flow) ====
  // Expected config in /js/config.js:
  //   COGNITO: { region, userPoolId, userPoolWebClientId, domain, redirectSignIn, redirectSignOut }

  aws_amplify.Amplify.configure({
    Auth: {
      region: cfg.AWS_REGION,
      userPoolId: cfg.COGNITO_USER_POOL_ID,
      userPoolWebClientId: cfg.COGNITO_APP_CLIENT_ID,
      oauth: {
        domain: cfg.COGNITO_DOMAIN,
        scope: ["email", "openid", "profile", "phone"],
        redirectSignIn: window.location.origin + "/post.html",
        redirectSignOut: window.location.origin + "/post.html",
        responseType: "token"
      }
    }
  });
  const { Auth, Hub } = aws_amplify;

  const $gate = $('#auth-gate');
  const $app = $('#app');
  const $loginBtn = $('#btn-login');
  const $logoutBtn = $('#btn-logout');
  let cognitoUsername = "";

  function showApp(){ $gate.addClass('hidden'); $app.removeClass('hidden'); }
  function showGate(){ $app.addClass('hidden'); $gate.removeClass('hidden'); $loginBtn.removeClass('hidden'); }

  // React to auth events
  Hub.listen('auth', ({ payload }) => {
    switch (payload.event) {
      case 'signIn':
        console.log('Signed in');
        showApp();
        break;
      case 'signIn_failure':
        console.warn('Sign in failed', payload);
        showGate();
        break;
      case 'signOut':
        console.log('Signed out');
        showGate();
        break;
    }
  });

  // Attempt to get current user, otherwise redirect to Hosted UI
  async function ensureSignedIn(){
    try {
      const user = await Auth.currentAuthenticatedUser();
      cognitoUsername = user.username || (user.attributes && user.attributes.preferred_username) || "";
      $('#p-user').val(cognitoUsername);
      showApp();
    } catch (e) {
      showGate();
      $loginBtn.on('click', () => Auth.federatedSignIn());
      Auth.federatedSignIn();
    }
  }

  await ensureSignedIn();

  // Helper: get the ID token to send to backend for JWT validation
  async function getIdToken(){
    const session = await Auth.currentSession();
    return session.getAccessToken().getJwtToken();
  }

  // ==== 2) Submit handler: send multipart form to backend /upload/ with Bearer token ====
  $('#post-form').on('submit', async function(e){
    e.preventDefault();
    const file = $('#p-image')[0].files[0];
    if(!file){ alert('Please choose an image'); return; }

    // Disable button UI
    const $btn = $('.btn.primary');
    $btn.prop('disabled', true).text('Uploading...');

    try {
      const token = await getIdToken();
      const formData = new FormData();
      formData.append('image', file);
      // UserID is now set from Cognito username, not from the form
      
      formData.append('UserID', cognitoUsername);
      formData.append('Country', $('#p-country').val());
      formData.append('City', $('#p-city').val().trim());
      formData.append('GeoLocation', $('#p-geo').val().trim());
      formData.append('Description', $('#p-desc').val().trim());
      formData.append('DetailedDescription', $('#p-ddesc').val().trim());
      formData.append('Category', $('#p-category').val());
      formData.append('KnowledgeType', $('#p-type').val());

      const resp = await fetch(`${cfg.BACKEND_BASE_URL}/upload/`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData,
      });

      if(!resp.ok){
        const t = await resp.text();
        throw new Error(`Upload failed: ${resp.status} ${t}`);
      }

      // Success -> go back to Explore
      window.location.href = '/main.html';
    } catch(err){
      console.error(err);
      alert('Failed to submit. Please try again.');
    } finally {
      $btn.prop('disabled', false).text('Submit');
    }
  });

  // Sign out
  $logoutBtn.on('click', () => Auth.signOut());
})();