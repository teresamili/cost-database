// individual_project_search.js

const filters = {};

// 监听按钮点击，记录选择的条件并添加选中样式
document.querySelectorAll(".region-btn").forEach((button) => {
  button.addEventListener("click", () => {
    const filter = button.dataset.filter;
    const value = button.dataset.value;
    filters[filter] = value !== "不限" ? value : null;

    // 移除同一组内其他按钮的选中状态
    document
      .querySelectorAll(`.region-btn[data-filter="${filter}"]`)
      .forEach((btn) => {
        btn.classList.remove("selected");
      });

    // 为当前点击的按钮添加选中状态
    button.classList.add("selected");
  });
});

// 点击确定按钮后发送查询请求
function performSearch() {
  const queryString = new URLSearchParams(filters).toString();
  fetch(`/search?${queryString}`)
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("results").innerHTML = JSON.stringify(
        data,
        null,
        2
      );
    });
}
