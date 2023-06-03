const express = require("express");
const dotenv = require("dotenv");
const cors = require("cors");
const { URL } = require("url");
const { Client } = require("pg");

dotenv.config();

const sslConfig = {
  rejectUnauthorized: false, // set to true in production
};

const app = express();
app.use(cors());
app.use(express.json());

const databaseUrl = process.env.database_url;
const urlParsed = new URL(databaseUrl);

const client = new Client({
  host: urlParsed.hostname,
  port: urlParsed.port,
  user: urlParsed.username,
  password: urlParsed.password,
  database: urlParsed.pathname.slice(1),
  ssl: true,
  ssl: sslConfig,
});

async function connectToDatabase() {
  try {
    await client.connect();
    console.log("Connected to the database");
  } catch (error) {
    console.error("Failed to connect to the database:", error);
  }
}

connectToDatabase(); // call the function to connect to the database
app.get("/", async (req, res) => {
  res.status(200).send({
    message: "Hello",
  });
});

app.post("/", async (req, res) => {
  // req is a list parameter include [keyword, website_name, laptop_type, price]
  let maxPrice = 200;
  let minPrice = 0;
  if (req.body.price !== "") {
    if (req.body.price === "lt15") {
      maxPrice = 15;
    } else if (req.body.price === "bt30") {
      minPrice = 30;
    } else {
      const values = req.body.price.split("-").map((value) => parseInt(value));
      minPrice = values[0];
      maxPrice = values[1];
    }
  }

  let query = `SELECT * FROM items WHERE name ILIKE '%${req.body.keyword}%'`;

  if (req.body.website_name !== "") {
    query += ` AND website ILIKE '${req.body.website_name}'`;
  }

  if (req.body.laptop_type !== "") {
      query += ` AND type ILIKE '${req.body.laptop_type}'`;
  }

  const results = await client.query(query);

  const response = { results: [] };
  results.rows.forEach(async (result) => {
    response.results.push({
      name: result.name,
      website: result.website,
      type: result.type,
      price: result.price,
      link: result.link,
      //  image: await getProductImage(result.link, result.website),
    });
  });

  console.log(response);
  res.status(200).send({ items: response });
});

app.listen(5000, () => console.log("Server started on http://localhost:5000"));
