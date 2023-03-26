import sanitizeHtml from "sanitize-html";
import { readFile, writeFile } from "fs";

//console.log("Sanitizing Html Code");

const default_img = "../../images/default_img.jpeg";
const default_svg = "../../images/default_img.svg";
const args = process.argv;
if (args.length != 4) {
  console.log("Usage: node sanitize_html <website_url> <folder>");
} else {
  const results_folder = args[3]
  const filepath = "experiments/" + results_folder + "/" + args[2] + "_raw.html";
  const excludedTags = ["script", "meta", "noscript", "svg", "path", "iframe"];
  readFile(filepath, (err, dirtyHtml) => {
    if (err) throw err;
    const cleanHtml = sanitizeHtml(dirtyHtml, {
      allowedTags: false,
      allowedAttributes: false,
      enforceHtmlBoundary: true,
      exclusiveFilter: function (frame) {
        return excludedTags.includes(frame.tag);
      },
      transformTags: {
        img: function (tagName, attribs) {
          if (attribs["data-src"]) {
            attribs["src"] = attribs["data-src"];
            delete attribs["data-src"];
          }
          if (attribs["data-lazy-src"]) {
            attribs["src"] = attribs["data-lazy-src"];
            delete attribs["data-lazy-src"];
          }
          if (attribs["data-srcset"]) {
            attribs["srcset"] = attribs["data-srcset"];
            delete attribs["data-srcset"];
          }
          if (attribs["data-lazy-srcset"]) {
            attribs["srcset"] = attribs["data-lazy-srcset"];
            delete attribs["data-lazy-srcset"];
          }
          for (const [key, value] of Object.entries(attribs)) {
            attribs[key] = value
              .replace(
                /(\s|^)[^ ]+\.(jpeg|jpg|png|webp)/g,
                "$1" + default_img
              )
              .replace(/(\s|^)[^ ]+\.svg/g, "$1" + default_svg);
          }
          return {
            tagName: "img",
            attribs: attribs,
          };
        },
        href: function (tagName, attribs) {
          if (attribs["data-src"]) {
            attribs["src"] = attribs["data-src"];
            delete attribs["data-src"];
          }
          if (attribs["data-lazy-src"]) {
            attribs["src"] = attribs["data-lazy-src"];
            delete attribs["data-lazy-src"];
          }
          if (attribs["data-srcset"]) {
            attribs["srcset"] = attribs["data-srcset"];
            delete attribs["data-srcset"];
          }
          if (attribs["data-lazy-srcset"]) {
            attribs["srcset"] = attribs["data-lazy-srcset"];
            delete attribs["data-lazy-srcset"];
          }
          for (const [key, value] of Object.entries(attribs)) {
            attribs[key] = value
              .replace(
                /(\s|^)[^ ]+\.(jpeg|jpg|png|webp)/g,
                "$1" + default_img
              )
              .replace(/(\s|^)[^ ]+\.svg/g, "$1" + default_svg);
          }
          return {
            tagName: "href",
            attribs: attribs,
          };
        },
        picture: function (tagName, attribs) {
          if (attribs["data-src"]) {
            attribs["src"] = attribs["data-src"];
            delete attribs["data-src"];
          }
          if (attribs["data-lazy-src"]) {
            attribs["src"] = attribs["data-lazy-src"];
            delete attribs["data-lazy-src"];
          }
          if (attribs["data-srcset"]) {
            attribs["srcset"] = attribs["data-srcset"];
            delete attribs["data-srcset"];
          }
          if (attribs["data-lazy-srcset"]) {
            attribs["srcset"] = attribs["data-lazy-srcset"];
            delete attribs["data-lazy-srcset"];
          }
          for (const [key, value] of Object.entries(attribs)) {
            attribs[key] = value
              .replace(
                /(\s|^)[^ ]+\.(jpeg|jpg|png|webp)/g,
                "$1" + default_img
              )
              .replace(/(\s|^)[^ ]+\.svg/g, "$1" + default_svg);
          }
          return {
            tagName: "picture",
            attribs: attribs,
          };
        },
        a: function (tagName, attribs) {
          if (attribs["data-src"]) {
            attribs["src"] = attribs["data-src"];
            delete attribs["data-src"];
          }
          if (attribs["data-lazy-src"]) {
            attribs["src"] = attribs["data-lazy-src"];
            delete attribs["data-lazy-src"];
          }
          if (attribs["data-srcset"]) {
            attribs["srcset"] = attribs["data-srcset"];
            delete attribs["data-srcset"];
          }
          if (attribs["data-lazy-srcset"]) {
            attribs["srcset"] = attribs["data-lazy-srcset"];
            delete attribs["data-lazy-srcset"];
          }
          for (const [key, value] of Object.entries(attribs)) {
            attribs[key] = value
              .replace(
                /(\s|^)[^ ]+\.(jpeg|jpg|png|webp)/g,
                "$1" + default_img
              )
              .replace(/(\s|^)[^ ]+\.svg/g, "$1" + default_svg);
          }
          return {
            tagName: "a",
            attribs: attribs,
          };
        },
        source: function (tagName, attribs) {
          if (attribs["data-src"]) {
            attribs["src"] = attribs["data-src"];
            delete attribs["data-src"];
          }
          if (attribs["data-lazy-src"]) {
            attribs["src"] = attribs["data-lazy-src"];
            delete attribs["data-lazy-src"];
          }
          if (attribs["data-srcset"]) {
            attribs["srcset"] = attribs["data-srcset"];
            delete attribs["data-srcset"];
          }
          if (attribs["data-lazy-srcset"]) {
            attribs["srcset"] = attribs["data-lazy-srcset"];
            delete attribs["data-lazy-srcset"];
          }
          for (const [key, value] of Object.entries(attribs)) {
            attribs[key] = value
              .replace(
                /(\s|^)[^ ]+\.(jpeg|jpg|png|webp)/g,
                "$1" + default_img
              )
              .replace(/(\s|^)[^ ]+\.svg/g, "$1" + default_svg);
          }
          return {
            tagName: "source",
            attribs: attribs,
          };
        },

        link: function (tagName, attribs) {
          if (attribs["data-src"]) {
            attribs["src"] = attribs["data-src"];
            delete attribs["data-src"];
          }
          if (attribs["data-lazy-src"]) {
            attribs["src"] = attribs["data-lazy-src"];
            delete attribs["data-lazy-src"];
          }
          if (attribs["data-srcset"]) {
            attribs["srcset"] = attribs["data-srcset"];
            delete attribs["data-srcset"];
          }
          if (attribs["data-lazy-srcset"]) {
            attribs["srcset"] = attribs["data-lazy-srcset"];
            delete attribs["data-lazy-srcset"];
          }
          for (const [key, value] of Object.entries(attribs)) {
            attribs[key] = value
              .replace(
                /(\s|^)[^ ]+\.(jpeg|jpg|png|webp)/g,
                "$1" + default_img
              )
              .replace(/(\s|^)[^ ]+\.svg/g, "$1" + default_svg);
          }
          return {
            tagName: "link",
            attribs: attribs,
          };
        },
        div: function (tagName, attribs) {
          if (attribs["data-src"]) {
            attribs["src"] = attribs["data-src"];
            delete attribs["data-src"];
          }
          if (attribs["data-lazy-src"]) {
            attribs["src"] = attribs["data-lazy-src"];
            delete attribs["data-lazy-src"];
          }
          if (attribs["data-srcset"]) {
            attribs["srcset"] = attribs["data-srcset"];
            delete attribs["data-srcset"];
          }
          if (attribs["data-lazy-srcset"]) {
            attribs["srcset"] = attribs["data-lazy-srcset"];
            delete attribs["data-lazy-srcset"];
          }
          for (const [key, value] of Object.entries(attribs)) {
            attribs[key] = value
              .replace(
                /(\s|^)[^ ]+\.(jpeg|jpg|png|webp)/g,
                "$1" + default_img
              )
              .replace(/(\s|^)[^ ]+\.svg/g, "$1" + default_svg);
          }
          return {
            tagName: "div",
            attribs: attribs,
          };
        },
        figure: function (tagName, attribs) {
          if (attribs["data-src"]) {
            attribs["src"] = attribs["data-src"];
            delete attribs["data-src"];
          }
          if (attribs["data-lazy-src"]) {
            attribs["src"] = attribs["data-lazy-src"];
            delete attribs["data-lazy-src"];
          }
          if (attribs["data-srcset"]) {
            attribs["srcset"] = attribs["data-srcset"];
            delete attribs["data-srcset"];
          }
          if (attribs["data-lazy-srcset"]) {
            attribs["srcset"] = attribs["data-lazy-srcset"];
            delete attribs["data-lazy-srcset"];
          }
          for (const [key, value] of Object.entries(attribs)) {
            attribs[key] = value
              .replace(
                /(\s|^)[^ ]+\.(jpeg|jpg|png|webp)/g,
                "$1" + default_img
              )
              .replace(/(\s|^)[^ ]+\.svg/g, "$1" + default_svg);
          }
          return {
            tagName: "figure",
            attribs: attribs,
          };
        },
        ol: "ul",
      },

      // transformTags: {
      // img: function (tagName, attribs) {
      // //if (attribs["data-src"]) {
      // //delete attribs["data-src"];
      // //}
      // //if (attribs["data-srcset"]) {
      // //delete attribs["data-srcset"];
      // //}
      // //if (attribs["data-lazy-src"]) {
      // //delete attribs["data-lazy-src"];
      // //}
      // //if (attribs["data-lazy-srcset"]) {
      // //delete attribs["data-lazy-src"];
      // //}
      // //if (attribs["srcset"]) {
      // //delete attribs["srcset"];
      // //}
      // //if (attribs["src"] && attribs.src.endsWith(".svg")) {
      // //attribs.src = default_svg;
      // //} else {
      // //attribs.src = default_img;
      // //}

      // // TODO: understand when to use width/height/size/
      // // reuse lazy-size in size or smthg
      // // try also adding alt
      // /*if (attribs["src"] && (!attribs["width"] && !attribs["height"] && !attribs["size"] && !attribs["sizes"])) {
      // // Download the image and look its size, then add size
      // const image = new Image();
      // image.onload = function() {
      // attribs.width= this.naturalWidth
      // attribs.height= this.naturalHeight
      // }
      // image.src = attribs["src"]
      // }
      // */
      // return {
      // tagName: "img",
      // attribs: attribs,
      // };
      // },
      // ol: "ul",
      // },
    });
    writeFile("experiments/" + results_folder + "/" + args[2] + ".html", cleanHtml, (err) => {
      if (err) throw err;
    });
    console.log(cleanHtml);
  });
}
