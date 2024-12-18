// pagination.js
function performSearch(apiUrl, filters, renderResults) {
  const queryString = new URLSearchParams(filters).toString();

  fetch(`${apiUrl}?${queryString}`)
    .then((response) => response.json())
    .then((data) => {
      const resultsElement = document.getElementById("results");
      resultsElement.innerHTML = "";

      if (!data.results || data.results.length === 0) {
        resultsElement.innerHTML =
          "<tr><td colspan='10'>没有符合条件的结果</td></tr>";
        return;
      }

      // 调用页面提供的渲染方法
      renderResults(data.results);

      // 渲染分页
      if (data.pagination) {
        renderPagination(data.pagination, filters, () =>
          performSearch(apiUrl, filters, renderResults)
        );
      }
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
      alert("数据加载失败，请稍后重试。");
    });
}

function renderPagination(pagination, filters, searchCallback) {
  const paginationElement = document.querySelector(".pagination");
  paginationElement.innerHTML = "";

  if (pagination.total_pages <= 1) return;

  const maxPagesToShow = 5;
  const startPage = Math.max(
    1,
    pagination.current_page - Math.floor(maxPagesToShow / 2)
  );
  const endPage = Math.min(
    pagination.total_pages,
    startPage + maxPagesToShow - 1
  );

  // 上一页
  if (pagination.current_page > 1) {
    createPageLink(
      paginationElement,
      "< 上一页",
      pagination.current_page - 1,
      filters,
      searchCallback
    );
  }

  // 页码
  for (let page = startPage; page <= endPage; page++) {
    createPageLink(
      paginationElement,
      page,
      page,
      filters,
      searchCallback,
      page === pagination.current_page
    );
  }

  // 下一页
  if (pagination.current_page < pagination.total_pages) {
    createPageLink(
      paginationElement,
      "下一页 >",
      pagination.current_page + 1,
      filters,
      searchCallback
    );
  }
}

function createPageLink(
  container,
  text,
  page,
  filters,
  searchCallback,
  isActive = false
) {
  const link = document.createElement("a");
  link.href = "#";
  link.textContent = text;
  if (isActive) link.classList.add("active");

  link.addEventListener("click", (event) => {
    event.preventDefault();
    filters.page = page; // 更新页码
    searchCallback();
  });

  container.appendChild(link);
}
