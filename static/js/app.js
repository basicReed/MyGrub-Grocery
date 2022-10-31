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

$("#search-form").submit(function () {
  const query = $("#query").val();
  return requestRcps(query);
});

async function requestRcps(query) {
  console.log("made it this far");
  let res = await axios.get(`/recipes/search/${query}`);
  console.log(res);
  let recipes = res.results;
  console.log(recipes);
  for (let rec of recipes) {
    let recipe = $(generateRecipeListHTML(rec));
    $("#recipe-list").append(recipe);
  }
}

function generateRecipeListHTML(rec) {
  // add in id to allow hover animation to select into recipe
  return `<a href="/recipes/${rec.id}/details">
  <div class="card" style="background-image: url(${rec.image})">
    <div class="food-info">
      <p>${rec.title} <br /><span>click for more info</span></p>
      <div class="favorite">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 93.3 80.6">
          <path
            d="M86.2 7c-9.4-9.4-24.6-9.4-33.9 0l-5.7 5.7L41 7C31.6-2.3 16.4-2.3 7 7c-9.3 9.4-9.3 24.6 0 34l5.7 5.7 33.9 33.9 33.9-33.9 5.7-5.7c9.4-9.4 9.4-24.6 0-34z"
          />
        </svg>
      </div>
    </div>
  </div>
</a>
`;
}
