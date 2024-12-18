document.addEventListener("DOMContentLoaded", function () {
  const filters = {}; // 存储筛选条件

  // 处理筛选按钮点击事件
  document.querySelectorAll(".region-btn").forEach((button) => {
    button.addEventListener("click", () => {
      const filter = button.getAttribute("price-filter");
      const value = button.getAttribute("price-value");

      // 更新筛选条件
      if (value === "不限") {
        delete filters[filter]; // 删除"不限"条件
      } else {
        filters[filter] = value; // 更新筛选条件
      }

      // 清除该行其他按钮的选中状态
      document
        .querySelectorAll(`.region-btn[price-filter="${filter}"]`)
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
    console.log("Performing search with filters:", filters);

    const queryInput = document.querySelector(".search-bar input");
    if (queryInput) {
      filters["search"] = queryInput.value.trim();
    }

    const queryString = new URLSearchParams(filters).toString();
    console.log("Generated Query String:", queryString);

    // 调用后端 API
    fetch(`/material-prices/search?${queryString}`)
      .then((response) => response.json())
      .then((price) => {
        console.log("Search Results (Debug):", price);

        const resultsElement = document.querySelector("tbody");
        resultsElement.innerHTML = "";

        if (!price || price.results.length === 0) {
          resultsElement.innerHTML =
            "<tr><td colspan='10'>没有符合条件的结果</td></tr>";
          return;
        }

        price.results.forEach((order, index) => {
          const row = document.createElement("tr");
          const projectId = order.project_id || "#";
          //定义table格式 “material-prices”是table id
          const table = document.getElementById("material-prices");

          row.innerHTML = `
            <td>${index + 1}</td>
            <td>${order.material_price.材料名称}</td>
            <td>${order.material_price.规格型号 || ""}</td>
            <td>${order.material_price.单位}</td>
            <td>${order.material_price.数量}</td>
            <td>${order.material_price.不含税单价}</td>
            <td>${order.material_price.合计}</td>
            <td>${order.project_basis}</td>
            <td>
              ${
                projectId !== "#"
                  ? `<a href="/individual-projects?project_id=${encodeURIComponent(
                      projectId
                    )}">${order.project_name || "未命名项目"}-${
                      order.unit_name || "未命名项目"
                    }</a>`
                  : `<span>${order.project_name || "未命名项目"}</span>`
              }
            </td>
          `;
          resultsElement.appendChild(row);
        });

        // 添加分页显示
        if (price.pagination) {
          renderPagination(price.pagination);
        }
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

    // 限制分页显示，只显示前后若广页
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
        event.preventDefault(); // 阻止页面跳转
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
