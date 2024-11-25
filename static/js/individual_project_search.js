const filters = {}; // 将 filters 变量定义在全局作用域

document.addEventListener("DOMContentLoaded", function () {

  // 监听按钮点击事件，每行只能选择一个值
  document.querySelectorAll(".region-btn").forEach((button) => {
    button.addEventListener("click", () => {
      const filter = button.getAttribute("data-filter");
      const value = button.getAttribute("data-value");

      console.log(`Button clicked: filter=${filter}, value=${value}`); // 调试信息

      // 更新 filters 对象中的选定值
      filters[filter] = value;

      // 移除当前行其他按钮的选中状态
      document
        .querySelectorAll(`.region-btn[data-filter="${filter}"]`)
        .forEach((btn) => {
          btn.classList.remove("selected");
        });

      // 为当前点击的按钮添加选中状态
      button.classList.add("selected", "active");
    });
  });
});

// 点击确定按钮后发送查询请求
function performSearch() {
  console.log("Filters before search:", filters);

  // 将筛选条件转换为查询字符串
  const queryString = new URLSearchParams(filters).toString();
  console.log("Generated Query URL:", `/search?${queryString}`);

  // 向后端发送筛选请求
  fetch(`/search?${queryString}`)
    .then((response) => response.json())
    .then((data) => {
      console.log("Received data:", data); // 打印接收到的数据
      const resultsElement = document.getElementById("results");

      if (resultsElement) {
        // 清空表格内容
        resultsElement.innerHTML = "";

        // 如果没有数据，提示空表信息
        if (data.length === 0) {
          resultsElement.innerHTML =
            "<tr><td colspan='10'>没有符合条件的结果</td></tr>";
          return;
        }

        // 遍历数据并插入新内容
        data.forEach((item) => {
          const row = document.createElement("tr");
          row.innerHTML = `
            <td>
              <a href="${item.url}">
                ${item.建设项目工程名称 || ""}
              </a>
            </td>
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
