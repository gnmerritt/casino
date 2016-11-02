exports.config =
  npm:
    enabled: true
  plugins:
    babel:
      presets: ['es2015', 'es2016', 'react', 'stage-0']
      pattern: /\.(js|es6|jsx)$/
  paths:
    public: 'matchmaker/static/'
    watched: ['matchmaker/webapp/']
  files:
    javascripts:
      joinTo:
        'vendor.js': /^(node_modules|vendor)/
        'app.js': /^matchmaker\/webapp\/js/
    stylesheets:
      joinTo:
        'vendor.css': /^(node_modules|vendor)/
        'app.css': /^matchmaker\/webapp\/css/

  overrides:
    production:
      optimize: true
      sourceMaps: false
