var path = require('path')
var utils = require('./utils')
var config = require('../config')
var vueLoaderConfig = require('./vue-loader.conf')

function resolve(dir) {
    return path.join(__dirname, '..', dir)
}

var webpack = require("webpack")

module.exports = {
    entry: {
        app: './src/main.js'
    },
    externals:{
        "element-ui":"ELEMENT",
        "vue":"Vue",
        'vue-router':'VueRouter',
        'vuex':'Vuex'
    },
    output: {
        path: config.build.assetsRoot,
        filename: '[name].js',
        publicPath: process.env.NODE_ENV === 'production'
            ? config.build.assetsPublicPath
            : config.dev.assetsPublicPath
    },
    resolve: {
        extensions: ['.js', '.vue', '.json'],
        alias: {
            'vue$': 'vue/dist/vue.esm.js',
            '@': resolve('src'),
            'scss_vars': '@/styles/vars.scss'
        }
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader',
                options: vueLoaderConfig
            },
            {
                   test: /\.js$/,
                   loader: 'babel-loader',  //注意elementUI的源码使用ES6需要解析
                   include: [resolve('src'), resolve('test'),resolve('/node_modules/bootstrap-vue/lib'),
                   resolve('/node_modules/element-ui/src'),resolve('/node_modules/element-ui/packages'),
                   resolve('/node_modules/highlight.js/lib')   // 在编译规则处添加报错模块目录
                   ]
            },
//            {
//                test: /\.js$/,
//                loader: 'babel-loader',
//                include: [resolve('src'), resolve('test')]
//            },
            {
                test: /\.(png|jpe?g|gif|svg)(\?.*)?$/,
                loader: 'url-loader',
                options: {
                    limit: 10000,
                    name: utils.assetsPath('img/[name].[hash:7].[ext]')
                }
            },
            {
                test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/,
                loader: 'url-loader',
                options: {
                    limit: 10000,
                    name: utils.assetsPath('fonts/[name].[hash:7].[ext]')
                }
            },
            {
                test: /element-ui.src.*?js$/,
                loader: 'babel-loader'
            }
        ]
    },
    // externals: {
    //     'AMap': 'AMap',
    //     'AMapUI': 'AMapUI'
    // },
    plugins: [
        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery"
        })
    ]
}
