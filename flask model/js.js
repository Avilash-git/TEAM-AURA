// JavaScript to handle form navigation and input conditions

let currentStep = 1; // Track the current step

// Function to show the current step and hide others
function showStep(step) {
    const steps = document.querySelectorAll('.form-step');
    steps.forEach((el, index) => {
        el.classList.toggle('active', index === step - 1); // Show only the active step
    });
}

// Move to the next step
function nextStep(current) {
    currentStep = current + 1;
    showStep(currentStep);
}

// Move to the previous step
function prevStep(current) {
    currentStep = current - 1;
    showStep(currentStep);
}

// Show or hide hip size input based on gender
function toggleHipInput() {
    const gender = document.getElementById('gender').value;
    const hipInput = document.getElementById('hip-input');
    if (gender === 'female') {
        hipInput.style.display = 'block';
    } else {
        hipInput.style.display = 'none';
    }
}

// Initialize form behavior
document.addEventListener('DOMContentLoaded', () => {
    showStep(currentStep);  // Start with the first step
    toggleHipInput();  // Ensure the hip input is hidden for males on page load

    // Form submission
    const form = document.getElementById('fitnessForm');
    form.addEventListener('submit', (e) => {
        e.preventDefault();  // Prevent the default form submission behavior

        // Gather form data
        const gender = document.getElementById('gender').value;
        const age = document.getElementById('age').value;
        const height = document.getElementById('height').value;
        const weight = document.getElementById('weight').value;
        const waist = document.getElementById('waist').value;
        const neck = document.getElementById('neck').value;
        const hip = gender === 'female' ? document.getElementById('hip').value : null;
        const workoutRoutine = document.getElementById('workoutRoutine').value;
        const fitnessGoal = document.getElementById('fitnessGoal').value;
        const injuriesSetbacks = document.getElementById('injuriesSetbacks').value;

        // Display collected data for debugging (you can handle it differently as needed)
        console.log({
            gender,
            age,
            height,
            weight,
            waist,
            neck,
            hip,
            workoutRoutine,
            fitnessGoal,
            injuriesSetbacks
        });

        // You can replace the console log with actual form handling logic (e.g., send the data to a server)

        // Display a success message or take further action
        alert("Form submitted successfully!");
    });
});
