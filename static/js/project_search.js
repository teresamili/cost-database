document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("search-input");
  const table = document.getElementById("project-table");
  const rows = table.querySelectorAll("tbody tr");

  if (!searchInput || !table) {
    console.error("搜索输入框或表格未找到，请检查 HTML 结构。");
    return;
  }

  searchInput.addEventListener("input", function () {
    const filterText = searchInput.value.toLowerCase(); // 获取输入内容并转为小写
    rows.forEach((row) => {
      const projectName = row
        .querySelector("td:nth-child(2)")
        .innerText.toLowerCase(); // 获取第二列内容
      if (projectName.includes(filterText)) {
        row.style.display = ""; // 显示匹配的行
      } else {
        row.style.display = "none"; // 隐藏不匹配的行
      }
    });
  });
});
