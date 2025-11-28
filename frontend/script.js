let currentTasks = [];

function addTaskToList() {
  const title = document.getElementById("t-title").value;
  const date = document.getElementById("t-date").value;
  const hours = document.getElementById("t-hours").value;
  const imp = document.getElementById("t-imp").value;

  if (!title || !date || !hours) {
    alert("Please fill in all fields");
    return;
  }

  const newTask = {
    title: title,
    due_date: date,
    estimated_hours: parseFloat(hours),
    importance: parseInt(imp),
    dependencies: [],
  };

  currentTasks.push(newTask);
  alert("Task Added! Total in list: " + currentTasks.length);

  document.getElementById("t-title").value = "";
}

function clearList() {
  currentTasks = [];
  document.getElementById("json-input").value = "";
  alert("List cleared");
}

async function analyzeTasks() {
  const resultsArea = document.getElementById("results-area");
  const errorMsg = document.getElementById("error-msg");
  const loading = document.getElementById("loading");
  const strategy = document.getElementById("strategy-select").value;
  const jsonInput = document.getElementById("json-input").value;

  errorMsg.style.display = "none";
  resultsArea.innerHTML = "";
  loading.style.display = "block";

  let finalPayload = [...currentTasks];

  if (jsonInput.trim() !== "") {
    try {
      const parsed = JSON.parse(jsonInput);
      finalPayload = finalPayload.concat(parsed);
    } catch {
      errorMsg.innerText = "Invalid JSON format.";
      errorMsg.style.display = "block";
      loading.style.display = "none";
      return;
    }
  }

  if (finalPayload.length === 0) {
    errorMsg.innerText = "No tasks to analyze.";
    errorMsg.style.display = "block";
    loading.style.display = "none";
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:8000/api/tasks/analyze/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        tasks: finalPayload,
        strategy: strategy,
      }),
    });

    if (!response.ok) throw new Error("API Error");

    const sortedTasks = await response.json();
    renderTasks(sortedTasks);
  } catch {
    errorMsg.innerText = "Error connecting to server. Is Django running?";
    errorMsg.style.display = "block";
  } finally {
    loading.style.display = "none";
  }
}

function renderTasks(tasks) {
  const container = document.getElementById("results-area");

  tasks.forEach((task) => {
    let priorityClass = "priority-medium";
    if (task.score > 50) priorityClass = "priority-high";
    if (task.score < 20) priorityClass = "priority-low";

    const html = `
            <div class="task-card ${priorityClass}">
                <span class="score-badge">Score: ${task.score}</span>
                <h3>${task.title}</h3>
                <div class="details">
                    Due: ${task.due_date} | Effort: ${task.estimated_hours}h | Importance: ${task.importance}/10
                </div>
                <div class="explanation">Why: ${task.explanation}</div>
            </div>
        `;

    container.innerHTML += html;
  });
}
