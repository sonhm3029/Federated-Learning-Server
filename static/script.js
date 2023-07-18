document.addEventListener("DOMContentLoaded", () => {
  let exeBtn = document.querySelector("#execute-fl");
  //   const eventSource = new EventSource(`${location.href}logs`);
  const serverLogs = document.querySelector(".server-logs");

  exeBtn.addEventListener("click", () => {
    fetch(`${location.href}execute-fl-server`, {
      method: "POST",
    })
      .then(async (res) => {
        console.log("res", await res.json());
      })
      .catch((err) => {
        console.log("POST ERR", err);
      });
  });

  setInterval(() => {
    fetch("/logs")
      .then(async (res) => {
        let result = await res.json();
        result = result?.message?.split("\n");
        let currentLogsList = document.querySelectorAll(".server-logs-item");

        if (result?.length > currentLogsList?.length) {
          let listNewLogs = result.slice(currentLogsList?.length);
          console.log(listNewLogs);
          for (let log of listNewLogs) {
            if (log) {
              let newLogElement = document.createElement("p");
              newLogElement.setAttribute("class", "server-logs-item");
              newLogElement.textContent = log;
              serverLogs.appendChild(newLogElement);
            }
          }
        }
      })
      .catch((err) => {
        console.log("Get LOGS error", err);
      });
  }, 5000);

  setInterval(() => {
    fetch("/stats")
      .then(async (res) => {
        let data = await res.json();
        console.log("SYS", data)

        for (let key in data) {
          let element = document.querySelector(`#${key}`);
          element.innerHTML = data[key] || "---";
        }
      })
      .catch((err) => {
        console.log("SYSTEM MONITOR FAIL", err);
      });
  }, 2000);

  //   eventSource.onmessage = (event) => {
  //     const logLine = event.data;
  //     console.log("STTTTT", logLine, "ENDDDĐ")
  //     const newLogElement = document.createElement("p");
  //     newLogElement.textContent = logLine;
  //     serverLogs.appendChild(newLogElement);
  //   };

  //   eventSource.onerror = (error) => {
  //     // Handle any errors
  //     console.log("SERVER error", error);
  //   };
});
