/******/ (function(modules) { // webpackBootstrap
/******/ 	// install a JSONP callback for chunk loading
/******/ 	function webpackJsonpCallback(data) {
/******/ 		var chunkIds = data[0];
/******/ 		var moreModules = data[1];
/******/ 		var executeModules = data[2];
/******/
/******/ 		// add "moreModules" to the modules object,
/******/ 		// then flag all "chunkIds" as loaded and fire callback
/******/ 		var moduleId, chunkId, i = 0, resolves = [];
/******/ 		for(;i < chunkIds.length; i++) {
/******/ 			chunkId = chunkIds[i];
/******/ 			if(Object.prototype.hasOwnProperty.call(installedChunks, chunkId) && installedChunks[chunkId]) {
/******/ 				resolves.push(installedChunks[chunkId][0]);
/******/ 			}
/******/ 			installedChunks[chunkId] = 0;
/******/ 		}
/******/ 		for(moduleId in moreModules) {
/******/ 			if(Object.prototype.hasOwnProperty.call(moreModules, moduleId)) {
/******/ 				modules[moduleId] = moreModules[moduleId];
/******/ 			}
/******/ 		}
/******/ 		if(parentJsonpFunction) parentJsonpFunction(data);
/******/
/******/ 		while(resolves.length) {
/******/ 			resolves.shift()();
/******/ 		}
/******/
/******/ 		// add entry modules from loaded chunk to deferred list
/******/ 		deferredModules.push.apply(deferredModules, executeModules || []);
/******/
/******/ 		// run deferred modules when all chunks ready
/******/ 		return checkDeferredModules();
/******/ 	};
/******/ 	function checkDeferredModules() {
/******/ 		var result;
/******/ 		for(var i = 0; i < deferredModules.length; i++) {
/******/ 			var deferredModule = deferredModules[i];
/******/ 			var fulfilled = true;
/******/ 			for(var j = 1; j < deferredModule.length; j++) {
/******/ 				var depId = deferredModule[j];
/******/ 				if(installedChunks[depId] !== 0) fulfilled = false;
/******/ 			}
/******/ 			if(fulfilled) {
/******/ 				deferredModules.splice(i--, 1);
/******/ 				result = __webpack_require__(__webpack_require__.s = deferredModule[0]);
/******/ 			}
/******/ 		}
/******/
/******/ 		return result;
/******/ 	}
/******/
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// object to store loaded and loading chunks
/******/ 	// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 	// Promise = chunk loading, 0 = chunk loaded
/******/ 	var installedChunks = {
/******/ 		"main": 0
/******/ 	};
/******/
/******/ 	var deferredModules = [];
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "public/js/";
/******/
/******/ 	var jsonpArray = window["webpackJsonp"] = window["webpackJsonp"] || [];
/******/ 	var oldJsonpFunction = jsonpArray.push.bind(jsonpArray);
/******/ 	jsonpArray.push = webpackJsonpCallback;
/******/ 	jsonpArray = jsonpArray.slice();
/******/ 	for(var i = 0; i < jsonpArray.length; i++) webpackJsonpCallback(jsonpArray[i]);
/******/ 	var parentJsonpFunction = oldJsonpFunction;
/******/
/******/
/******/ 	// add entry module to deferred list
/******/ 	deferredModules.push([0,"vendors"]);
/******/ 	// run deferred modules when ready
/******/ 	return checkDeferredModules();
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/js/helpers/canUseWebp.js":
/*!**************************************!*\
  !*** ./src/js/helpers/canUseWebp.js ***!
  \**************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony default export */ __webpack_exports__[\"default\"] = (() => {\n  const elem = document.createElement('canvas');\n\n  if (elem.getContext && elem.getContext('2d')) {\n    return elem.toDataURL('image/webp').indexOf('data:image/webp') === 0;\n  }\n\n  return false;\n});\n\n//# sourceURL=webpack:///./src/js/helpers/canUseWebp.js?");

/***/ }),

/***/ "./src/js/helpers/lazyLoad.js":
/*!************************************!*\
  !*** ./src/js/helpers/lazyLoad.js ***!
  \************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var lozad__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! lozad */ \"./node_modules/lozad/dist/lozad.min.js\");\n/* harmony import */ var lozad__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(lozad__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _canUseWebp__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./canUseWebp */ \"./src/js/helpers/canUseWebp.js\");\n\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (() => {\n  const element = '.lazy';\n  const changeAttr = 'data-srcset';\n  const changeAttrBg = 'data-background-image';\n\n  if (Object(_canUseWebp__WEBPACK_IMPORTED_MODULE_1__[\"default\"])() === true) {\n    const lazyBgItems = document.querySelectorAll(element);\n    lazyBgItems.forEach(item => {\n      if (item.hasAttribute(changeAttr)) {\n        const file = item.getAttribute(changeAttr).split('.');\n\n        if (file[1] !== 'gif') {\n          item.setAttribute(changeAttr, `${file[0]}.webp`);\n        }\n      }\n\n      if (item.hasAttribute(changeAttrBg)) {\n        const fileBg = item.getAttribute(changeAttrBg).split('.');\n\n        if (fileBg[1] !== 'gif') {\n          item.setAttribute(changeAttrBg, `${fileBg[0]}.webp`);\n        }\n      }\n    });\n  }\n\n  const el = document.querySelectorAll(element);\n  lozad__WEBPACK_IMPORTED_MODULE_0___default()(el).observe();\n});\n\n//# sourceURL=webpack:///./src/js/helpers/lazyLoad.js?");

/***/ }),

/***/ "./src/js/main.js":
/*!************************!*\
  !*** ./src/js/main.js ***!
  \************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _helpers_lazyLoad__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./helpers/lazyLoad */ \"./src/js/helpers/lazyLoad.js\");\n/* harmony import */ var _modules_animationScroll__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./modules/animationScroll */ \"./src/js/modules/animationScroll.js\");\n/* harmony import */ var _modules_menuMobile__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./modules/menuMobile */ \"./src/js/modules/menuMobile.js\");\n// import $ from 'jquery';\n// eslint-disable-next-line no-unused-vars\n\n\n\nObject(_modules_animationScroll__WEBPACK_IMPORTED_MODULE_1__[\"default\"])();\nObject(_modules_menuMobile__WEBPACK_IMPORTED_MODULE_2__[\"default\"])();\n\n//# sourceURL=webpack:///./src/js/main.js?");

/***/ }),

/***/ "./src/js/modules/animationScroll.js":
/*!*******************************************!*\
  !*** ./src/js/modules/animationScroll.js ***!
  \*******************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony default export */ __webpack_exports__[\"default\"] = (() => {\n  document.querySelectorAll('.jsScrollTo[href^=\"#\"').forEach(link => {\n    link.addEventListener('click', function (e) {\n      e.preventDefault();\n      let href = this.getAttribute('href').substring(1);\n      const scrollTarget = document.getElementById(href);\n      const topOffset = document.querySelector('.header').offsetHeight + 20;\n      const elementPosition = scrollTarget.getBoundingClientRect().top;\n      const offsetPosition = elementPosition - topOffset;\n      window.scrollBy({\n        top: offsetPosition,\n        behavior: 'smooth'\n      });\n    });\n  });\n});\n\n//# sourceURL=webpack:///./src/js/modules/animationScroll.js?");

/***/ }),

/***/ "./src/js/modules/menuMobile.js":
/*!**************************************!*\
  !*** ./src/js/modules/menuMobile.js ***!
  \**************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony default export */ __webpack_exports__[\"default\"] = (() => {\n  let menuBtn = document.querySelector('.header__menuBurger'); //document.getElementById('menuBtn');\n\n  let mobileWrap = document.querySelector('.header__listMobileWrap');\n  let body = document.querySelector('body');\n\n  menuBtn.onclick = () => {\n    menuBtn.classList.toggle('open-menu');\n    mobileWrap.classList.toggle('open-menu');\n    body.classList.toggle('fixed-page');\n  };\n});\n\n//# sourceURL=webpack:///./src/js/modules/menuMobile.js?");

/***/ }),

/***/ 0:
/*!******************************!*\
  !*** multi ./src/js/main.js ***!
  \******************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("module.exports = __webpack_require__(/*! C:\\Users\\lilia\\OneDrive\\Рабочий стол\\cola\\algotrader\\src\\js\\main.js */\"./src/js/main.js\");\n\n\n//# sourceURL=webpack:///multi_./src/js/main.js?");

/***/ })

/******/ });