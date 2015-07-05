exports.config =
  modules:
    definition: false
    wrapper: false
  paths:
    public: 'matchmaker/static/'
  files:
    javascripts:
      joinTo:
        'vendor.js': /^(bower_components|vendor)/
        'app.js': /^matchmaker\/webapp\/js/
    stylesheets:
      joinTo:
        'vendor.css': /^(bower_components|vendor)/
        'app.css': /^matchmaker\/webapp\/css/

  overrides:
    production:
      optimize: true
      sourceMaps: false
