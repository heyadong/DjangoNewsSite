var gulp = require("gulp")
var cssnano = require('gulp-cssnano');
var concat =  require('gulp-concat');
var rename = require("gulp-rename");
var uglify = require("gulp-uglify");
var imagemin = require("gulp-imagemin");
var cache = require("gulp-cache");
var bs = require("browser-sync");
var sass = require('gulp-sass');
var path ={
    "css_path":"./src/css/*.*",
    "image_path":"./src/image/*.*", // 所有格式的图片
    "js_path":"./src/js/*.js", // .js结尾的文件
    "dist_path":"./dist/",
    "html_path":'./templates/**/*.html'
};
//html
// gulp.task("html",function () {
//     gulp.src(path.html_path)
//         .pipe(bs.stream())
// });


// css 压缩任务
gulp.task('css',function () {
    gulp.src(path.css_path)
        .pipe(sass().on("error",sass.logError))
        .pipe(cssnano())
        .pipe(rename({"suffix":".min"}))
        .pipe(gulp.dest(path.dist_path+'css/'))
        // .pipe(bs.stream())

});
gulp.task("js",function () {
    gulp.src(path.js_path)
        .pipe(uglify())
        .pipe(rename({"suffix":".min"}))
        .pipe(gulp.dest(path.dist_path+"js/"))
        // .pipe(bs.stream())

});
gulp.task("imagemin",function(){
    gulp.src(path.image_path)
        .pipe(cache(imagemin()))
        .pipe(gulp.dest(path.dist_path+"image/"))



});
gulp.task("watch",function () {
    // gulp.watch(path.html_path,['html']);
    gulp.watch(path.css_path,["css"]);
    gulp.watch(path.js_path,["js"]);
    gulp.watch(path.image_path,["imagemin"])

});
//初始化"browser-sync"
// gulp.task("bs",function () {
//     bs.init({
//         'server':{
//             'basedir':'./'
//         }
//     });
// });
// 执行gulp默认任务
gulp.task("default",['watch']);

