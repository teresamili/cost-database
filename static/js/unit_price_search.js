document.addEventListener("DOMContentLoaded", function () {
  const filters = {}; // 存储筛选条件

  // 处理筛选按钮点击事件
  document.querySelectorAll(".region-btn").forEach((button) => {
    button.addEventListener("click", () => {
      const filter = button.getAttribute("data-filter");
      const value = button.getAttribute("data-value");

      // 更新筛选条件
      if (value === "不限") {
        delete filters[filter]; // 删除"不限"条件
      } else {
        filters[filter] = value; // 更新筛选条件
      }

      // 清除该行其他按钮的选中状态
      document
        .querySelectorAll(`.region-btn[data-filter="${filter}"]`)
        .forEach((btn) => {
          btn.classList.remove("selected", "active");
        });

      // 设置当前按钮为选中状态
      button.classList.add("selected", "active");

      console.log("Updated Filters:", filters); // 调试输出
    });
  });

  // 点击确定按钮触发查询
  document
    .querySelector(".sure button")
    .addEventListener("click", performSearch);

  function performSearch() {
    console.log("Performing search with filters:", filters); // 打印当前的筛选条件

    const queryInput = document.querySelector(".search-bar input");
    if (queryInput) {
      filters["search"] = queryInput.value.trim();
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
          console.log("Item Data:", item); // 调试每条记录

          const row = document.createElement("tr");
          // 修改 projectId 提取路径
          const projectId =
            item.project_id ||
            (item.unit_price && item.unit_price.project_id) ||
            "#";
          //定义table格式 “unit_prices”是table id
          const table = document.getElementById("unit_prices");

          row.innerHTML = `
    <td>${index + 1}</td>
    <td>${item.unit_price.项目编码}</td>
    <td>${item.unit_price.项目名称}</td>
    <td>${item.unit_price.项目特征描述}</td>
    <td>${item.unit_price.计量单位}</td>
    <td>${item.unit_price.工程量}</td>
    <td>${item.unit_price.综合单价}</td>
    <td>${item.unit_price.综合合价}</td>
    <td>${item.project_basis}</td>
    <td>
        ${
          projectId !== "#"
            ? `<a href="/individual-projects?project_id=${encodeURIComponent(
                projectId
              )}">${item.project_name || "未命名项目"}-${
                item.unit_name || "未命名项目"}</a>`
            : `<span>${item.project_name || "未命名项目"}</span>`
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
