// --- CRUD CLÁSICO DE TAREAS ---
// Funciones para crear, modificar, eliminar y ver tareas independientes

// Configuración de la API
const API_BASE_URL = '';

// Utilidad para mostrar mensajes
function showMessage(elementId, message, isError = false) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.className = `message-box ${isError ? 'error' : 'success'}`;
    element.style.display = 'block';
    setTimeout(() => {
        element.style.display = 'none';
    }, 5000);
}

// --- CRUD clásico de tareas ---
async function createTask(event) {
    event.preventDefault();
    const taskData = {
        title: document.getElementById('createTitle').value,
        description: document.getElementById('createDescription').value,
        priority: document.getElementById('createPriority').value,
        effort_hours: parseInt(document.getElementById('createEffortHours').value),
        status: document.getElementById('createStatus').value,
        assigned_to: document.getElementById('createAssignedTo').value
    };
    try {
        const response = await fetch(`${API_BASE_URL}/tasks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(taskData)
        });
        if (!response.ok) throw new Error('Error al crear la tarea');
        await response.json();
        showMessage('createResult', 'Tarea creada exitosamente');
        document.getElementById('createTaskForm').reset();
    } catch (error) {
        showMessage('createResult', error.message, true);
    }
}

async function loadTasks() {
    const taskId = document.getElementById('viewTaskId').value;
    const taskList = document.getElementById('taskList');
    taskList.innerHTML = '';
    try {
        let url = taskId ? `${API_BASE_URL}/tasks/${taskId}` : `${API_BASE_URL}/tasks`;
        const response = await fetch(url);
        if (!response.ok) throw new Error('Error al cargar las tareas');
        const data = await response.json();
        if (data.error) {
            taskList.innerHTML = `<p class="no-tasks">${data.error}</p>`;
            return;
        }
        const tasks = Array.isArray(data.tasks) ? data.tasks : (Array.isArray(data) ? data : [data]);
        if (tasks.length === 0) {
            taskList.innerHTML = '<p class="no-tasks">No se encontraron tareas</p>';
            return;
        }
        tasks.forEach(task => {
            const taskElement = document.createElement('div');
            taskElement.className = 'task-item';
            taskElement.innerHTML = `
                <h4>${task.title} <span class="task-id">[ID: ${task.id}]</span></h4>
                <ul class="task-fields">
                    <li><strong>Descripción:</strong> ${task.description ?? 'null'}</li>
                    <li><strong>Prioridad:</strong> ${task.priority ?? 'null'}</li>
                    <li><strong>Esfuerzo (horas):</strong> ${task.effort_hours ?? 'null'}</li>
                    <li><strong>Estado:</strong> ${task.status ?? 'null'}</li>
                    <li><strong>Asignado a:</strong> ${task.assigned_to ?? 'null'}</li>
                    <li><strong>user_story_id:</strong> ${task.user_story_id ?? 'null'}</li>
                    <li><strong>created_at:</strong> ${task.created_at ?? 'null'}</li>
                </ul>
            `;
            taskList.appendChild(taskElement);
        });
    } catch (error) {
        taskList.innerHTML = `<p class="no-tasks">${error.message}</p>`;
    }
}

async function updateTask(event) {
    event.preventDefault();
    const taskId = document.getElementById('updateTaskId').value;
    const taskData = {};
    const title = document.getElementById('updateTitle').value;
    const description = document.getElementById('updateDescription').value;
    const priority = document.getElementById('updatePriority').value;
    const effortHours = document.getElementById('updateEffortHours').value;
    const status = document.getElementById('updateStatus').value;
    const assignedTo = document.getElementById('updateAssignedTo').value;
    const userStoryId = document.getElementById('updateUserStoryId').value;
    if (title) taskData.title = title;
    if (description) taskData.description = description;
    if (priority) taskData.priority = priority;
    if (effortHours) taskData.effort_hours = parseInt(effortHours);
    if (status) taskData.status = status;
    if (assignedTo) taskData.assigned_to = assignedTo;
    if (userStoryId) taskData.user_story_id = parseInt(userStoryId);
    if (Object.keys(taskData).length === 0) {
        showMessage('updateResult', 'Por favor, complete al menos un campo para actualizar', true);
        return;
    }
    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(taskData)
        });
        if (!response.ok) throw new Error('Error al actualizar la tarea');
        await response.json();
        showMessage('updateResult', 'Tarea actualizada exitosamente');
        document.getElementById('updateTaskForm').reset();
    } catch (error) {
        showMessage('updateResult', error.message, true);
    }
}

async function deleteTask() {
    const taskId = document.getElementById('deleteTaskId').value;
    if (!taskId) {
        showMessage('deleteResult', 'Por favor ingrese un ID de tarea', true);
        return;
    }
    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, { method: 'DELETE' });
        if (!response.ok) throw new Error('Error al eliminar la tarea');
        showMessage('deleteResult', 'Tarea eliminada exitosamente');
        document.getElementById('deleteTaskId').value = '';
    } catch (error) {
        showMessage('deleteResult', error.message, true);
    }
}

// --- ACCIONES DE IA SOBRE TAREAS ---
// Funciones para describir, categorizar, estimar y auditar tareas usando IA

async function describeTask() {
    const taskId = document.getElementById('describeTaskId').value;
    if (!taskId) {
        showMessage('describeResult', 'Por favor ingrese un ID de tarea', true);
        return;
    }
    try {
        const response = await fetch(`${API_BASE_URL}/ai/tasks/describe`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ task_id: parseInt(taskId) })
        });
        if (!response.ok) throw new Error('Error al generar la descripción');
        await response.json();
        showMessage('describeResult', 'Descripción generada exitosamente. Ver detalles en la lista de tareas.');
    } catch (error) {
        showMessage('describeResult', error.message, true);
    }
}

async function categorizeTask() {
    const taskId = document.getElementById('categorizeTaskId').value;
    if (!taskId) {
        showMessage('categorizeResult', 'Por favor ingrese un ID de tarea', true);
        return;
    }
    try {
        const response = await fetch(`${API_BASE_URL}/ai/tasks/categorize`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ task_id: parseInt(taskId) })
        });
        if (!response.ok) throw new Error('Error al categorizar la tarea');
        const result = await response.json();
        showMessage('categorizeResult', `Categoría sugerida: ${result.category}`);
    } catch (error) {
        showMessage('categorizeResult', error.message, true);
    }
}

async function estimateTask() {
    const taskId = document.getElementById('estimateTaskId').value;
    if (!taskId) {
        showMessage('estimateResult', 'Por favor ingrese un ID de tarea', true);
        return;
    }
    try {
        const response = await fetch(`${API_BASE_URL}/ai/tasks/estimate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ task_id: parseInt(taskId) })
        });
        if (!response.ok) throw new Error('Error al estimar la tarea');
        const result = await response.json();
        showMessage('estimateResult', `Estimación sugerida: ${result.effort_hours} horas`);
    } catch (error) {
        showMessage('estimateResult', error.message, true);
    }
}

async function auditTask() {
    const taskId = document.getElementById('auditTaskId').value;
    if (!taskId) {
        showMessage('auditResult', 'Por favor ingrese un ID de tarea', true);
        return;
    }
    try {
        const response = await fetch(`${API_BASE_URL}/ai/tasks/audit`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ task_id: parseInt(taskId) })
        });
        if (!response.ok) throw new Error('Error al auditar la tarea');
        await response.json();
        showMessage('auditResult', 'Auditoría generada exitosamente. Ver detalles en la lista de tareas.');
    } catch (error) {
        showMessage('auditResult', error.message, true);
    }
}

// --- GESTIÓN AVANZADA DE HISTORIAS DE USUARIO ---
// Funciones para crear, consultar, desglosar historias de usuario y ver tareas asociadas

// (Aquí irían las funciones de historias de usuario, ya separadas)
// ...

// --- CONTROL DE SECCIONES ---
function showSection(sectionId) {
    const sections = ['mainMenu', 'crudSection', 'iaSection', 'userStoriesSection'];
    sections.forEach(id => {
        document.getElementById(id).style.display = (id === sectionId) ? 'block' : 'none';
    });
}

async function createUserStory(event) {
    event.preventDefault();
    const prompt = document.getElementById('userStoryPrompt').value;
    const resultBox = document.getElementById('createUserStoryResult');
    resultBox.style.display = 'block';
    resultBox.textContent = '';
    if (!prompt) {
        resultBox.textContent = 'Introduce un prompt para la historia de usuario.';
        resultBox.className = 'message-box error';
        return;
    }
    resultBox.innerHTML = 'Generando historia de usuario...';
    fetch(`${API_BASE_URL}/user-stories`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            resultBox.textContent = data.error;
            resultBox.className = 'message-box error';
        } else {
            resultBox.textContent = 'Historia de usuario creada correctamente.';
            resultBox.className = 'message-box success';
            document.getElementById('createUserStoryForm').reset();
        }
    })
    .catch(e => {
        resultBox.textContent = e.message || 'Error al crear historia de usuario.';
        resultBox.className = 'message-box error';
    });
}

async function consultUserStoryById() {
    const userStoryId = document.getElementById('consultUserStoryId').value;
    const resultBox = document.getElementById('consultUserStoryResult');
    resultBox.style.display = 'block';
    resultBox.textContent = '';
    let url = `${API_BASE_URL}/user-stories`;
    if (userStoryId) {
        url += `?id=${userStoryId}`;
    }
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Error al consultar la historia de usuario');
        const data = await response.json();
        if (data.error) {
            resultBox.textContent = data.error;
            resultBox.className = 'message-box error';
            return;
        }
        // Si es una sola historia
        if (data.id) {
            resultBox.innerHTML = `<strong>ID:</strong> ${data.id}<br><strong>Historia:</strong> ${data.description}<br><strong>Prompt:</strong> ${data.prompt ?? ''}`;
        } else if (Array.isArray(data.user_stories)) {
            // Si es un array de historias
            resultBox.innerHTML = data.user_stories.map(us => `<div style='margin-bottom:10px;'><strong>ID:</strong> ${us.id}<br><strong>Historia:</strong> ${us.description}<br><strong>Prompt:</strong> ${us.prompt ?? ''}</div>`).join('');
        } else {
            resultBox.textContent = 'No se encontraron historias de usuario.';
        }
        resultBox.className = 'message-box success';
    } catch (e) {
        resultBox.textContent = e.message || 'Error al consultar historia de usuario.';
        resultBox.className = 'message-box error';
    }
}

async function generateTasksById() {
    const userStoryId = document.getElementById('generateTasksUserStoryId').value;
    const resultBox = document.getElementById('generateTasksResult');
    resultBox.style.display = 'block';
    resultBox.textContent = '';
    if (!userStoryId) {
        resultBox.textContent = 'Por favor ingresa un ID de historia de usuario.';
        resultBox.className = 'message-box error';
        return;
    }
    resultBox.innerHTML = 'Generando tareas para la historia de usuario...';
    try {
        const response = await fetch(`${API_BASE_URL}/user-stories/${userStoryId}/generate-tasks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const data = await response.json();
        if (!response.ok || data.error) {
            resultBox.textContent = data.error || 'Error al generar tareas para la historia de usuario.';
            resultBox.className = 'message-box error';
            return;
        }
        resultBox.textContent = 'Tareas generadas correctamente para la historia de usuario.';
        resultBox.className = 'message-box success';
    } catch (e) {
        resultBox.textContent = e.message || 'Error al generar tareas para la historia de usuario.';
        resultBox.className = 'message-box error';
    }
}

async function consultTasksForUserStory() {
    const userStoryId = document.getElementById('tasksUserStoryId').value;
    const resultBox = document.getElementById('tasksByIdResult');
    resultBox.style.display = 'block';
    resultBox.textContent = '';
    if (!userStoryId) {
        resultBox.textContent = 'Por favor ingresa un ID de historia de usuario.';
        resultBox.className = 'message-box error';
        return;
    }
    try {
        const response = await fetch(`${API_BASE_URL}/user-stories/${userStoryId}/tasks`);
        const data = await response.json();
        if (!response.ok || data.error) {
            resultBox.textContent = data.error || 'Error al consultar tareas de la historia de usuario.';
            resultBox.className = 'message-box error';
            return;
        }
        if (!Array.isArray(data.tasks) || data.tasks.length === 0) {
            resultBox.textContent = 'No hay tareas asociadas a esta historia de usuario.';
            resultBox.className = 'message-box error';
            return;
        }
        resultBox.innerHTML = data.tasks.map(task => `
            <div style='margin-bottom:10px;'>
                <strong>ID:</strong> ${task.id}<br>
                <strong>Título:</strong> ${task.title}<br>
                <strong>Descripción:</strong> ${task.description ?? ''}<br>
                <strong>Prioridad:</strong> ${task.priority ?? ''}<br>
                <strong>Esfuerzo (horas):</strong> ${task.effort_hours ?? ''}<br>
                <strong>Estado:</strong> ${task.status ?? ''}<br>
                <strong>Asignado a:</strong> ${task.assigned_to ?? ''}
            </div>
        `).join('');
        resultBox.className = 'message-box success';
    } catch (e) {
        resultBox.textContent = e.message || 'Error al consultar tareas de la historia de usuario.';
        resultBox.className = 'message-box error';
    }
}

window.onload = function() { showSection('mainMenu'); }; 