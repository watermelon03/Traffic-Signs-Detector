module.exports = function(grunt) {
  grunt.loadNpmTasks('grunt-contrib-coffee');
  grunt.loadNpmTasks('grunt-simple-mocha');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-browserify');
  grunt.initConfig({
    simplemocha: { dev: {
      src: 'spec/electron_cookies_spec.js',
      options: {
        reporter: 'spec',
        slow: 200,
        timeout: 1000
      }
    }
  },
    watch: { all: {
      files: [
        'src/*.js',
        'spec/*.js'
      ],
      tasks: [
        'test'
      ]
    }
  },
    browserify: {
      client: {
        src: ['src/index.js'],
        dest: 'dist/electron-cookies.js',
      },
      options: {
        alias: {
          'net': './node_modules/net-browserify/browser.js'
        }
      }
    }
  });
  grunt.registerTask('test', 'simplemocha:dev');
  grunt.registerTask('default', [
    'test',
    'browserify'
  ]);
};
