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
      button.classList.add("selected");
    });
  });
});

// 点击确定按钮后发送查询请求
function performSearch() {
  // 检查是否所有行都有选择
  const requiredFilters = [
    "project_location",
    "construction_nature",
    "price_basis",
    "cost_type",
    "road_grade",
  ];
  for (const filter of requiredFilters) {
    if (!filters[filter]) {
      alert(`请为${filter}选择一个选项`);
      return;
    }
  }

  // 将查询条件转换为 URL 参数
  const queryString = new URLSearchParams(filters).toString();
  fetch(`/search?${queryString}`)
    .then((response) => response.json())
    .then((data) => {
      console.log("Received data:", data); // 打印接收到的数据
      const resultsElement = document.getElementById("results");
      if (resultsElement) {
        // 清空原有内容
        resultsElement.innerHTML = "";

        // 检查接收到的数据是否为空
        if (data.length === 0) {
          resultsElement.innerHTML =
            "<tr><td colspan='10'>没有符合条件的结果</td></tr>";
          return;
        }

        // 遍历数据并插入新内容
        data.forEach((item) => {
          const row = document.createElement("tr");
          row.innerHTML = `
            <td>${item.建设项目工程名称 || ""}</td>
            <td>${item.项目地点 || ""}</td>
            <td>${item.建设性质 || ""}</td>
            <td>${item.价格基准期 || ""}</td>
            <td>${item.造价类型 || ""}</td>
            <td>${item.道路等级 || ""}</td>
            <td>${item.单项工程费用 || ""}</td>
            <td>${item.道路长度指标 || ""}</td>
            <td>${item.道路面积指标 || ""}</td>
            <td>${item.单位工程 || ""}</td>
          `;
          resultsElement.appendChild(row);
        });
      } else {
        console.error("Element with id 'results' not found.");
      }
    });
}