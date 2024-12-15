document.addEventListener("DOMContentLoaded", function () {
  const filters = {}; // 存储筛选条件

  // 处理筛选按钮点击事件
  document.querySelectorAll(".region-btn").forEach((button) => {
    button.addEventListener("click", () => {
      const filter = button.getAttribute("data-filter");
      const value = button.getAttribute("data-value");
      // 更新筛选条件
      filters[filter] = value;

      // 清除该行其他按钮的选中状态
      document
        .querySelectorAll(`.region-btn[data-filter="${filter}"]`)
        .forEach((btn) => {
          btn.classList.remove("selected", "active");
        });

      // 设置当前按钮为选中状态
      button.classList.add("selected", "active");
    });
  });

  // 点击确定按钮触发
  document
    .querySelector(".sure button")
    .addEventListener("click", performSearch);

  // 调试和修复 performSearch 方法
  function performSearch() {
    console.log("Performing search with filters:", filters); // 打印当前的筛选条件

    const queryInput = document.querySelector(".search-bar input");
    if (queryInput) {
      filters["search"] = queryInput.value.trim();
    }

    // 获取筛选条件：年份和造价类型
    const selectedYear = document.querySelector(
      ".region-btn[data-filter='price_basis'].selected"
    );
    const selectedCostType = document.querySelector(
      ".region-btn[data-filter='cost_type'].selected"
    );

    if (selectedYear && selectedYear.getAttribute("data-value") !== "不限") {
      filters["price_basis"] = selectedYear.getAttribute("data-value");
    } else {
      delete filters["price_basis"];
    }

    if (
      selectedCostType &&
      selectedCostType.getAttribute("data-value") !== "不限"
    ) {
      filters["cost_type"] = selectedCostType.getAttribute("data-value");
    } else {
      delete filters["cost_type"];
    }

    const queryString = new URLSearchParams(filters).toString();
    console.log("Generated Query String:", queryString); // 打印生成的查询字符串

    // 调用后端 API
    fetch(`/unit-prices/search?${queryString}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP Error: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        console.log("Search Results (Debug):", data); // 打印返回的数据

        const resultsElement = document.querySelector("tbody");
        resultsElement.innerHTML = "";

        if (!data || data.results.length === 0) {
          resultsElement.innerHTML =
            "<tr><td colspan='10'>没有符合条件的结果</td></tr>";
          renderPagination({ total_pages: 1, current_page: 1 }); // 渲染单页分页器
          return;
        }

        data.results.forEach((item, index) => {
          const row = document.createElement("tr");
          const projectId = item.project_id
            ? encodeURIComponent(item.project_id)
            : "";

          row.innerHTML = `
    <td>${index + 1}</td>
    <td>${item.unit_price.项目编码}</td>
    <td>${item.unit_price.项目名称}</td>
    <td>${item.unit_price.项目特征描述}</td>
    <td>${item.unit_price.计量单位}</td>
    <td>${item.unit_price.工程量}</td>
    <td>${item.unit_price.综合单价}</td>
    <td>${item.unit_price.综合合价}</td>
    <td>
       ${
         item.project_id
           ? `<a href="/individual-projects?project_id=${encodeURIComponent(
               item.project_id
             )}">
                      ${item.project_name}
                    </a>`
           : `<span>${item.project_name}</span>`
       }
    </td>
  `;
          resultsElement.appendChild(row);
        });

        // 重新渲染分页器
        renderPagination(data.pagination);
      })
      .catch((error) => {
        console.error("Error during fetch:", error);
        alert("查询失败，请稍后重试！");
      });
    //调试输出
    if (selectedYear) {
      console.log("Selected Year:", selectedYear.getAttribute("data-value"));
    }
    if (selectedCostType) {
      console.log(
        "Selected Cost Type:",
        selectedCostType.getAttribute("data-value")
      );
    }
  }

  function renderPagination(pagination) {
    const paginationElement = document.querySelector(".pagination");
    paginationElement.innerHTML = "";

    if (!pagination || !pagination.total_pages || pagination.total_pages <= 1) {
      console.log("Only 1 page, hiding pagination");
      return; // 如果只有 1 页或 total_pages 未定义，不显示分页器
    }

    // 限制分页显示，只显示前后若干页
    const maxPagesToShow = 5;
    const startPage = Math.max(
      1,
      pagination.current_page - Math.floor(maxPagesToShow / 2)
    );
    const endPage = Math.min(
      pagination.total_pages,
      startPage + maxPagesToShow - 1
    );

    // 添加 "上一页" 按钮
    if (pagination.current_page > 1) {
      const prevLink = document.createElement("a");
      prevLink.href = "#";
      prevLink.textContent = "< 上一页";
      prevLink.addEventListener("click", (event) => {
        event.preventDefault();
        filters["page"] = pagination.current_page - 1;
        performSearch();
      });
      paginationElement.appendChild(prevLink);
    }

    // 添加页码按钮
    for (let page = startPage; page <= endPage; page++) {
      const pageLink = document.createElement("a");
      pageLink.href = "#";
      pageLink.textContent = page;

      if (page === pagination.current_page) {
        pageLink.classList.add("active");
      }

      pageLink.addEventListener("click", (event) => {
        event.preventDefault(); // 防止页面跳转
        filters["page"] = page; // 更新当前页码
        performSearch(); // 重新执行查询
      });

      paginationElement.appendChild(pageLink);
    }

    // 添加 "下一页" 按钮
    if (pagination.current_page < pagination.total_pages) {
      const nextLink = document.createElement("a");
      nextLink.href = "#";
      nextLink.textContent = "下一页 >";
      nextLink.addEventListener("click", (event) => {
        event.preventDefault();
        filters["page"] = pagination.current_page + 1;
        performSearch();
      });
      paginationElement.appendChild(nextLink);
    }
  }
});
