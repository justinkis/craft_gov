document.addEventListener("DOMContentLoaded", () => {
    const inputs = document.querySelectorAll(".quantity-input");
    const remainingWeightEl = document.getElementById("remaining-weight");
    const requiredMaterialsEl = document.getElementById("required-materials");

    const MAX_WEIGHT = 2000; // Максимальный вес в кг
    const MAX_MATERIALS = 20000; // Максимальное количество материалов

    function calculateTotals() {
        let totalWeight = 0;
        let totalMaterials = 0;

        inputs.forEach((input) => {
            const quantity = parseInt(input.value) || 0;
            const cost = parseFloat(input.dataset.cost);
            const weight = parseFloat(input.dataset.weight);

            totalWeight += quantity * weight;
            totalMaterials += quantity * cost;
        });

        remainingWeightEl.textContent = (MAX_WEIGHT - totalWeight).toFixed(2);
        requiredMaterialsEl.textContent = totalMaterials.toFixed(0);
    }

    function enforceLimits(input) {
        const quantity = parseInt(input.value) || 0;
        const cost = parseFloat(input.dataset.cost);
        const weight = parseFloat(input.dataset.weight);

        const totalWeight = Array.from(inputs).reduce(
            (sum, inp) => sum + (inp === input ? 0 : (parseInt(inp.value) || 0) * parseFloat(inp.dataset.weight)),
            0
        );

        const totalMaterials = Array.from(inputs).reduce(
            (sum, inp) => sum + (inp === input ? 0 : (parseInt(inp.value) || 0) * parseFloat(inp.dataset.cost)),
            0
        );

        const maxAllowedByWeight = Math.floor((MAX_WEIGHT - totalWeight) / weight);
        const maxAllowedByMaterials = Math.floor((MAX_MATERIALS - totalMaterials) / cost);
        const maxAllowed = Math.min(maxAllowedByWeight, maxAllowedByMaterials);

        if (quantity > maxAllowed) {
            input.value = maxAllowed > 0 ? maxAllowed : 0;
        }
    }

    function allowOnlyNumbers(event) {
        const charCode = event.charCode || event.keyCode;
        // Разрешаем только цифры (0-9) и управление (Backspace, Delete, Tab, Arrow keys)
        if (charCode !== 0 && (charCode < 48 || charCode > 57)) {
            event.preventDefault();
        }
    }

    // Привязка событий `input` и `keypress` к полям ввода
    inputs.forEach((input) => {
        input.addEventListener("input", () => {
            enforceLimits(input);
            calculateTotals();
        });
        input.addEventListener("keypress", allowOnlyNumbers);
    });
});
