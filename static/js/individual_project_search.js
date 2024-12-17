document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded and parsed");

  // 全局筛选条件对象
  const filters = {};

  // 为所有按钮绑定点击事件
  document.querySelectorAll(".region-btn").forEach((button) => {
    button.addEventListener("click", () => {
      const filter = button.getAttribute("data-filter");
      const value = button.getAttribute("data-value");

      console.log(`Button clicked: filter=${filter}, value=${value}`);

      // 更新全局筛选条件
      filters[filter] = value;

      // 清除当前行的其他按钮的选中状态
      document
        .querySelectorAll(`.region-btn[data-filter="${filter}"]`)
        .forEach((btn) => {
          btn.classList.remove("selected", "active");
        });

      // 为当前点击的按钮添加选中状态
      button.classList.add("selected", "active");

      // 执行条件搜索（如果搜索框为空）
      if (!document.getElementById("search-input").value.trim()) {
        performSearch();
      }
    });
  });

  // 实时输入过滤项目名称
  const searchInput = document.getElementById("search-input");
  searchInput.addEventListener("input", function () {
    const filterText = searchInput.value.trim(); // 获取输入内容，去除前后空格
    console.log("实时搜索项目名称:", filterText);

    if (filterText) {
      // 执行实时过滤
      filterByProjectName(filterText);
    } else {
      // 如果搜索框为空，执行条件搜索
      performSearch();
    }
  });

  // 处理筛选条件搜索
  document
    .querySelector(".sure button")
    .addEventListener("click", performSearch);

  // 执行筛选条件搜索
  function performSearch() {
    console.log("Filters before search:", filters);

    // 将筛选条件转换为查询字符串
    const queryString = new URLSearchParams(filters).toString();
    console.log("Generated Query URL:", `/search?${queryString}`);

    // 模拟发送请求
    fetch(`/search?${queryString}`)
      .then((response) => response.json())
      .then((data) => {
        console.log("Received data:", data);
        const resultsElement = document.getElementById("results");

        if (resultsElement) {
          // 清空表格
          resultsElement.innerHTML = "";

          if (data.length === 0) {
            resultsElement.innerHTML =
              "<tr><td colspan='10'>没有符合条件的结果</td></tr>";
            return;
          }

          // 填充数据，确保项目名称保留链接
          data.forEach((item) => {
            const row = document.createElement("tr");

            // 项目名称添加<a>标签
            const projectName = item.建设项目工程名称 || "";
            const projectNameLink = `<a href="/project/${item.id}" target="_blank">${projectName}</a>`;

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
        } else {
          console.error("Element with id 'results' not found.");
        }
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        alert("查询失败，请稍后重试。");
      });
  }

  // 项目名称实时过滤函数
  function filterByProjectName(searchText) {
    const rows = document.querySelectorAll("#results tr");

    rows.forEach((row) => {
      const projectNameCell = row.querySelector("td:nth-child(1)"); // 获取第一列的单元格
      const projectName = projectNameCell
        ? projectNameCell.innerText.trim()
        : "";

      // 实时匹配输入框内容
      if (projectName.includes(searchText)) {
        row.style.display = ""; // 显示匹配的行
      } else {
        row.style.display = "none"; // 隐藏不匹配的行
      }
    });
  }
});
