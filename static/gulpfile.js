// gulpfile.js
// Include plugins
var gulp = require('gulp'),
    less = require('gulp-less'),
    imagemin = require('gulp-imagemin'),
    notify = require('gulp-notify'),
    connect = require('gulp-connect');

var path = {
        less: [
            './less/base/base.less',
            './less/icons/icons.less',
            './less/reward_input/reward_input.less',
            './less/reward_input/reward_query.less',
            './less/reward_single/reward_single.less',
            './less/edit/edit-pack-add.less',
            './less/gmt_manage/gmt_manage.less',
            './less/gmt_registration/gmt_registration.less',
            './less/gmt_competence/gmt_competence.less',
            './less/ann_edit/ann_edit.less',
            './less/ann_manage/ann_manage.less',
            './less/package_edit/package_edit.less',
            './less/cdk_create/cdk_create.less',
            './less/cdk_info/cdk_info.less',
            './less/marquee_create/marquee_create.less',
            './less/marquee_info/marquee_info.less',
            './less/marquee_manage/marquee_manage.less',
            './less/player_search/player_search.less',
            './less/player_choice/player_choice.less',
            './less/player_info/player_info.less',
            './less/mail_timing/mail_timing.less',
            './less/mail/mail.less',
            './less/ban_info/ban_info.less',
            './less/login/login.less',
            './less/search_info/search_info.less',
            './less/game_update/game_update.less',
            './less/game_address/game_address.less',
            './less/ann_option/ann_option.less',
            './less/package_option/package_option.less',
            './less/game_dynamic/game_dynamic.less',
            './less/player_pay/player_pay.less',
            './less/server_version_update/server_version_update.less'
        ],
        lessAll: './less/*/*.less',
        conUrl: [
            './less',
            './javascript'
        ],
        images: './img/**/*'
    }

//less
gulp.task('less', function() {
    gulp.src(path.lessAll)
        .pipe(less())
        .pipe(gulp.dest('./less'));
});

//less
gulp.task('lessBuild', function() {
    gulp.src(path.less)
        .pipe(less())
        .pipe(gulp.dest('./dist'));
});

//imagemin
gulp.task('imagemin', function () {
    gulp.src('./static/**/img/*')
        .pipe(
            imagemin({
                progressive: true
            })
        )
        .pipe(gulp.dest('./dist/image'))
        .pipe(
            notify({
                onLast: 'true',
                message: 'Images task complete'
            })
        );
});

gulp.task('webserver', function() {
    connect.server({
        root: path.conUrl,
    });
});

//watch
gulp.task('watch', function() {
    gulp.watch(path.lessAll, ['less']);
    //gulp.watch(path.images, ['imagemin']);
});

//default
gulp.task('default', ['less', 'webserver', 'watch']);
