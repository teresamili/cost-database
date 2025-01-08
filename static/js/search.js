document.addEventListener("DOMContentLoaded", function () {
  // 搜索输入框
  const searchInput = document.querySelector("#search-input");
  const searchHiddenInput = document.querySelector(
    `form.search-condition input[name="search"]`
  );

  if (searchInput && searchHiddenInput) {
    // 同步搜索框的值到筛选条件表单中的隐藏字段
    searchInput.addEventListener("input", function () {
      searchHiddenInput.value = searchInput.value.trim();
    });
  }

  // 筛选条件按钮点击事件
  document.querySelectorAll(".region-btn").forEach((button) => {
    button.addEventListener("click", () => {
      const filter = button.getAttribute("data-filter");
      const value = button.getAttribute("data-value");

      // 更新隐藏字段
      const hiddenInput = document.querySelector(`input[name="${filter}"]`);
      if (hiddenInput) {
        hiddenInput.value = value;
      }

      // 更新按钮状态
      document
        .querySelectorAll(`.region-btn[data-filter="${filter}"]`)
        .forEach((btn) => btn.classList.remove("active"));
      button.classList.add("active");
    });
  });
});
