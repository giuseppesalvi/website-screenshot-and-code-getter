import sanitizeHtml from "sanitize-html";
import { readFile, writeFile } from "fs";

//console.log("Sanitizing Html Code");

const default_img = "../images/default_img.jpeg";
const args = process.argv;
if (args.length != 4) {
  console.log("Usage: node sanitize_html <website_url> <test_name>");
} else {
  const filepath = "results/" + args[2] + ".html";
  const excludedTags = ["script", "meta", "noscript", "svg", "path"];
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
        img: sanitizeHtml.simpleTransform("img", {
          src: default_img,
          srcset: default_img,
        }),
        "ol": "ul",
      },
    });
    writeFile("results/" + args[2] + "_" + args[3] +".html", cleanHtml, (err) => {
      if (err) throw err;
    });
    console.log(cleanHtml);
  });
}
