const form = document.querySelector("form");
const submitButton = form.querySelector('input[type="submit"]');
const sortSelect = document.getElementById("sort");

function convertToProductArray(list) {
  return Array.from(list, function (li) {
    const name = li.querySelector("h3").textContent;
    const price = parseInt(li.querySelector("p").textContent);
    const link = li.querySelector("a").href;
    return { name, price, link };
  });
}

function updateProductList() {
  const productList = document.querySelector(".product-list");
  const productArray = convertToProductArray(
    productList.querySelectorAll("li")
  );
  return productArray;
}

function sortProducts(products, sortOption) {
  let sortedProducts;
  console.log("Sorting products:", products);
  switch (sortOption) {
    case "low-high":
      sortedProducts = products.sort((a, b) => {
        const priceA = parseInt(a.price.replace(/\./g, ""));
        const priceB = parseInt(b.price.replace(/\./g, ""));
        return priceA - priceB;
      });
      console.log("Sorted products (low-high):", sortedProducts);
      return sortedProducts;
    case "high-low":
      sortedProducts = products.sort((a, b) => {
        const priceA = parseInt(a.price.replace(/\./g, ""));
        const priceB = parseInt(b.price.replace(/\./g, ""));
        return priceB - priceA;
      });
      console.log("Sorted products (high-low):", sortedProducts);
      return sortedProducts;
    default:
      console.log("Unsorted products:", products);
      return products;
  }
}

function displayProducts(products) {
  const sort = document.getElementById("sort-bar");
  if (products.length == 0) {
    console.log("No products found");
    sort.style.display = "none";
  } else {
    console.log("Displaying products");
    sort.style.display = "block";
  }
  const productList = document.querySelector(".product-list");
  productList.innerHTML = "";

  products.forEach(function (p) {
    const li = document.createElement("li");
    li.classList.add("product");

    const h3 = document.createElement("h3");
    h3.textContent = p.name;
    li.appendChild(h3);

    const price = document.createElement("p");
    temp = p.price.toLocaleString();
    price.textContent = `${temp} đ`; // Định dạng giá
    li.appendChild(price);

    const a = document.createElement("a");
    a.href = p.link;
    a.textContent = "Visit website";
    a.target = "_blank";
    li.appendChild(a);

    productList.appendChild(li);
  });
}

sortSelect.addEventListener("change", () => {
  const productArray = updateProductList();
  sortValue = sortSelect.value;
  const sortedProducts = sortProducts(productArray, sortValue);
  displayProducts(sortedProducts);
});

function searchProducts(searchQuery, storeFilter, brandFilter, priceFilter) {
  fetch("https://web-crawler-gbk2.onrender.com/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      keyword: searchQuery,
      website_name: storeFilter,
      laptop_type: brandFilter,
      price: priceFilter,
    }),
  })
    .then((response) => response.json()) // parse response as JSON
    .then((data) => {
      console.log(data.items.results);
      displayProducts(data.items.results); // log response to console
    })
    .catch((error) => {
      console.error(error); // log any errors to console
    });
}

submitButton.addEventListener("click", function (e) {
  e.preventDefault(); // prevent the form from submitting
  // your code to store user input goes here
  const searchQuery = document.querySelector("#search-bar").value;
  const brandFilter = document.querySelector("#brand-filter").value;
  const storeFilter = document.querySelector("#store-filter").value;
  const priceFilter = document.querySelector("#price-filter").value;

  searchProducts(searchQuery, storeFilter, brandFilter, priceFilter);
});
