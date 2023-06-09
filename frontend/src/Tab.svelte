<script>
    export let category;
    let changeTab = async (tab) => {
        if (tab != category) {
            category = tab;
            if (tab == "Alcohol") {
                document.getElementById("Groceries").classList.remove("active");
                document.getElementById("Groceries").classList.add("inactive");
                document.getElementById("Alcohol").classList.add("active");
                document.getElementById("Alcohol").classList.remove("inactive");
            } else {
                document
                    .getElementById("Groceries")
                    .classList.remove("inactive");
                document.getElementById("Groceries").classList.add("active");
                document.getElementById("Alcohol").classList.add("inactive");
                document.getElementById("Alcohol").classList.remove("active");
            }
        }
    };
</script>

<div>
    <button
        class="active"
        id="Groceries"
        on:click={() => changeTab("Groceries")}>Groceries</button
    >
    <button class="inactive" id="Alcohol" on:click={() => changeTab("Alcohol")}
        >Alcohol</button
    >
</div>

<style>
    div {
        display: flex;
    }
    button {
        border: 0px solid red;
        width: 50%;
        font-size: large;
        height: 2rem;
        margin: 0px;
        padding: 0px;
        font-weight: bold;
        text-align: center;
        color: hsl(208, 49%, 82%);
    }
    .active {
        background-color: rgb(108, 44, 42);
    }
    .inactive {
        background-color: rgb(131, 35, 0);
    }
</style>
