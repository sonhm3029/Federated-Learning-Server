document.addEventListener("DOMContentLoaded", () => {
  let exeBtn = document.querySelector("#execute-fl");

  exeBtn.addEventListener("click", () => {
    fetch(`${location.href}/execute-fl-server`, {
      method: "POST",
    })
      .then(async (res) => {
        console.log("res", await res.json());
      })
      .catch((err) => {
        console.log("POST ERR", err);
      });
  });
});
