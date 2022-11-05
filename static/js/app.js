// MyGrub JS File

/////////////////////////
// Side Bar Navigation//
///////////////////////
$(".btn").click(function () {
  $(this).toggleClass("click");
  $(".sidebar").toggleClass("show");
  console.log("Ive been clicked");
});

$(".feat-btn").click(function () {
  $("nav ul .feat-show").toggleClass("show");
  $("nav ul .first").toggleClass("rotate");
});

$(".serv-btn").click(function () {
  $("nav ul .serv-show").toggleClass("show1");
  $("nav ul .second").toggleClass("rotate");
});

$("nav ul li").click(function () {
  $(this).addClass("active").siblings().removeClass("active");
});

////////////////////////
// Search Bar Func/////
//////////////////////

$("#search-form").submit(async (e) => {
  e.preventDefault();
  const query = $("#query").val();
  const checkedRadios = document.querySelectorAll(
    'input[type="checkbox"]:checked'
  );
  const values = Array.from(checkedRadios, (radio) =>
    radio.value.toLowerCase()
  );
  console.log(values);
  await requestRcps(query, values);
});

async function requestRcps(query, intol) {
  let res = await axios.get(`/recipes/search/${query}/${intol}`);
  let recipes = res.data.results;

  // Diplay recipes found or message if none
  if (recipes.length === undefined || recipes.length == 0) {
    $("#results-none").removeClass("hidden");
  } else {
    $("#results-none").addClass("hidden");
    $("#recipe-list").empty();
    for (let rec of recipes) {
      let recipe = $(generateRecipeListHTML(rec));
      $("#recipe-list").append(recipe);
    }
  }
}

////////////////////////
// Recipe Card Func/////
//////////////////////

// Generates Recipe Card with route to recipe details
function generateRecipeListHTML(rec) {
  return `
<a href="/recipes/${rec.id}/details">
  <div class="card" style="background-image: url(${rec.image})">
    <div class="food-info">
      <p>${rec.title} <br /><span>click for more info</span></p>
      <button class="favorite" value="${rec.id}">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 93.3 80.6">
          <path
            d="M86.2 7c-9.4-9.4-24.6-9.4-33.9 0l-5.7 5.7L41 7C31.6-2.3 16.4-2.3 7 7c-9.3 9.4-9.3 24.6 0 34l5.7 5.7 33.9 33.9 33.9-33.9 5.7-5.7c9.4-9.4 9.4-24.6 0-34z"
          />
        </svg>
      </button>
    </div>
  </div>
  </>
`;
}

// Handles Favorites Button on Card
$("body").on("click", ".favorite", async (e) => {
  e.preventDefault();
  e.stopPropagation();
  btn = e.target.closest("button");
  console.log("clicked");
  console.log("button value: ", btn.value);
  btn.classList.toggle("js-is-selected");
  await axios.post(`/recipes/${btn.value}/favorite`);
});

////////////////////////
// Grocery List Func/////
//////////////////////

// Recipe Details Page Add Form
$("#add-groc-form").submit(async (e) => {
  e.preventDefault();

  const checked = document.querySelectorAll('input[type="checkbox"]:checked');
  console.log("checked:", checked);
  const values = Array.from(checked, (check) => check.value);
  console.log("values:", values);
  await axios.post(`/groceries/add/${values}`);
  flash = $(".ing-added");
  flash.removeClass("hidden");
});

// Grocery Page Remove by ID Button
$(".remove").click(async (e) => {
  e.preventDefault();
  const item = e.target.parentElement;
  const ing_id = item.value;

  item.closest("li").remove();
  await axios.post(`/groceries/remove/${ing_id}`);
});

// Grocery Page Remove ALL Button
$(".Remove-all").click(function () {
  console.log("Removed All");
  wrap = $(".confirm-wrap");
  wrap.removeClass("hidden");
});

///////////////////////////////////////////
// Grocery Page Delete Confirmation Func//
/////////////////////////////////////////

// Cancel Delete All Groceries
$(".cancel").click(function () {
  console.log("cancel");
  wrap = $(".confirm-wrap");
  wrap.addClass("hidden");
});

// Confirm Delete All Groceries
$(".delete").click(async function () {
  await axios.post("/groceries/remove/all");
  $("#grocery-list").empty();
  wrap = $(".confirm-wrap");
  wrap.addClass("hidden");
});
