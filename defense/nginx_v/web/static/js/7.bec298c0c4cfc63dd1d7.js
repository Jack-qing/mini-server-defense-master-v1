webpackJsonp([7],{Cc7p:function(t,e){},xCHB:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=a("v6mm"),r=a("zBK0"),i={name:"index",components:{Navbar:n.a},data:function(){return{activeIndex:"1",net:{},time:"",tagNum:""}},methods:{},created:function(){var t=this,e=this.$route.query.repotag;Object(r.c)(e).then(function(e){t.net=e.data}),Object(r.e)(e).then(function(e){t.tagNum=e.data["Tag Name"].length}),this.time=(new Date).toLocaleString()}},s={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("header",[a("navbar")],1),t._v(" "),a("section",{staticClass:"main"},[a("p",{staticClass:"main-nav"},[a("router-link",{attrs:{to:"/"}},[t._v("\n        总览\n      ")]),t._v(" "),a("span",[t._v("> >"+t._s(this.$route.query.repotag))])],1),t._v(" "),a("section",{staticClass:"main-wrapper"},[a("div",{staticClass:"brief"},[a("p",[t._v(t._s(this.$route.query.repotag))]),t._v(" "),""===t.tagNum?a("span",[a("i",[t._v("标签数：")]),t._v("--")]):a("span",[a("i",[t._v("标签数：")]),t._v(t._s(t.tagNum)+"个 ")]),t._v(" "),a("span",[a("i",[t._v("网页更新时间：")]),t._v(t._s(this.time))])]),t._v(" "),a("div",{staticClass:"sub-nav"},[a("el-menu",{attrs:{"default-active":t.activeIndex,mode:"horizontal"}},[a("el-menu-item",{attrs:{index:"1"}},[a("router-link",{attrs:{to:{path:"index",query:{repotag:this.$route.query.repotag}}}},[t._v("\n              概述\n            ")])],1),t._v(" "),a("el-menu-item",{attrs:{index:"2"}},[a("router-link",{attrs:{to:{path:"strategy",query:{repotag:this.$route.query.repotag}}}},[t._v("\n              策略\n            ")])],1),t._v(" "),a("el-menu-item",{attrs:{index:"3"}},[a("router-link",{attrs:{to:{path:"content",query:{repotag:this.$route.query.repotag}}}},[t._v("\n              内容\n            ")])],1),t._v(" "),a("el-menu-item",{attrs:{index:"4"}},[a("router-link",{attrs:{to:{path:"security",query:{repotag:this.$route.query.repotag}}}},[t._v("\n              安全\n            ")])],1)],1)],1),t._v(" "),a("transition",{attrs:{name:"fade",mode:"out-in"}},[a("keep-alive",[a("router-view",{attrs:{net:t.net}})],1)],1)],1)])])},staticRenderFns:[]};var o=a("VU/8")(i,s,!1,function(t){a("Cc7p")},"data-v-28a9bd93",null);e.default=o.exports}});
//# sourceMappingURL=7.bec298c0c4cfc63dd1d7.js.map