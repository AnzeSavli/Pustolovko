const express = require("express");
const bodyParser = require("body-parser");
const fs = require("fs");
const path = require("path");
const readline = require("readline");

const TOKEN =
    "!A%D*G-KaPdSgVkYp3s6v9y/B?E(H+MbQeThWmZq4t7w!z%C&F)J@NcRfUjXn2r5u8x/A?D(G-KaPdSgVkYp3s6v9y$B&E)H@MbQeThWmZq4t7w!z%C*F-JaNdRfUjXn2r5u8x/A?D(G+KbPeShVkYp3s6v9y$B&E)H@McQfTjWnZq4t7w!z%C*F-JaNdRgUkXp2s5u8x/A?D(G+KbPeShVmYq3t6w9y$B&E)H@McQfTjWnZr4u7x!A%C*F-JaNd";

const app = express();

app.use(bodyParser.json());
app.set("view engine", "ejs");
app.use(express.static(path.join(__dirname, "public")));

app.get("/", (req, res) => {
    res.render("index");
});

async function processLineByLine(filepath) {
    const fileStream = fs.createReadStream(filepath);
    const data = new Array();
    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity,
    });

    for await (const line of rl) {
        let low = 0;
        let high = data.length;

        while (low < high) {
            var mid = (low + high) >> 1;

            if (data[mid].split("-")[1] < line.split("-")[1]) low = mid + 1;
            else high = mid;
        }
        // console.log(`insert ${line} at ${low}`);
        data.splice(low, 0, line);
    }
    return data;
}

app.get("/:level", (req, res) => {
    filepath = "./scores/" + req.params.level + ".txt";
    processLineByLine(filepath).then((val) => {
        res.render("score", {
            data: val,
            level: req.params.level,
        });
    });
});

app.post("/score", (req, res) => {
    if (req.headers.safety_token) {
        if (req.headers.safety_token == TOKEN) {
            filepath = "./scores/" + req.body.level + ".txt";
            const data = req.body.player + "-" + req.body.score + "\n";
            fs.writeFile(filepath, data, { flag: "a+" }, (err) => {
                if (err) console.error(err);
            });
            res.status(200).send("Score saved");
        } else res.status(403).send("Incorrect token");
    } else res.status(403).send("Token not provided.");
});

app.listen(3000, () => console.log(`Example app listening on port 3000!`));
