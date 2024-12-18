document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded and parsed");

  const filters = {};

  // 1. 按钮点击筛选
  document.querySelectorAll(".region-btn").forEach((button) => {
    button.addEventListener("click", () => {
      const filter = button.getAttribute("data-filter");
      const value = button.getAttribute("data-value");

      // 更新筛选条件
      filters[filter] = value;

      // 清除其他按钮状态，添加选中状态
      document
        .querySelectorAll(`.region-btn[data-filter="${filter}"]`)
        .forEach((btn) => btn.classList.remove("selected", "active"));
      button.classList.add("selected", "active");

      performSearch();
    });
  });

  // 2. 搜索框关键词搜索
  const searchInput = document.getElementById("search-input");
  searchInput.addEventListener("input", () => {
    filters["search"] = searchInput.value.trim();
    performSearch();
  });

  // 3. 执行搜索请求
  function performSearch() {
    const queryString = new URLSearchParams(filters).toString();
    console.log("请求的 URL:", `/individual-projects?${queryString}`); // 打印请求的 URL

    fetch(`/individual-projects?${queryString}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => updateTable(data))
      .catch((error) => {
        console.error("查询失败:", error);
        alert("查询失败，请稍后重试。");
      });
  }


  // 4. 更新表格内容
  function updateTable(data) {
    const resultsElement = document.getElementById("results");
    resultsElement.innerHTML = "";

    if (data.length === 0) {
      resultsElement.innerHTML =
        "<tr><td colspan='12'>没有符合条件的结果</td></tr>";
      return;
    }

    data.forEach((item) => {
      const row = document.createElement("tr");
      const projectNameLink = `<a href="${item.url}" target="_blank">${item.建设项目工程名称}</a>`;

      row.innerHTML = `
        <td>${projectNameLink}</td>
        <td>${item.项目地点 || ""}</td>
        <td>${item.建设性质 || ""}</td>
        <td>${item.价格基准期 || ""}</td>
        <td>${item.造价类型 || ""}</td>
        <td>${item.道路等级 || ""}</td>
        <td>${item.单项工程费用 || ""}</td>
        <td>${item.道路全长 || ""}</td>
        <td>${item.道路长度指标 || ""}</td>
        <td>${item.道路总面积 || ""}</td>
        <td>${item.道路面积指标 || ""}</td>
        <td>${item.单位工程 || ""}</td>
      `;
      resultsElement.appendChild(row);
    });
  }


});
