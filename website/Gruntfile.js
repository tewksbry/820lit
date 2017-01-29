module.exports = function(grunt) {
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),

		concurrent: {
			target: {
				tasks: ['watch:sass'],
				options: {
					logConcurrentOutput: true
				}
			}
		},
		watch: {
			index: {
				options: {
					livereload: true
				},
				files: ['./index.html', './assets/css/main.css'],
				tasks: []
			},
			sass: {
        options: {
          livereload: true
        },

				files: ['assets/sass/main.scss', './index.html'],
				tasks: ['sass']
			}
		},
		express: {
			all: {
				options: {
					port: 3000,
					hostname: 'localhost',
					bases: ["./"],
					livereload: true
				}
			}
		},
		sass: {
			dist: {
				options: {
					sourcemap: 'none'
				},
				files: {
					'./assets/css/main.css': './assets/sass/main.scss'
				}
			}
		}
	});

	grunt.loadNpmTasks('grunt-contrib-watch');
	grunt.loadNpmTasks('grunt-express');
	grunt.loadNpmTasks('grunt-contrib-sass');
	grunt.loadNpmTasks('grunt-concurrent');
	grunt.registerTask('server', ['sass','express', 'concurrent']);
};
