CSS = """

.column {
    border: round $accent;
    padding-right: 1;
    padding-left: 1;
    width: 1fr;
    scrollbar-size-vertical: 1;
    scrollbar-color: green;
}
.text {
    border: round green;
}


.selected {
    border: round deepskyblue;
    background: #DDB8B8;   
    color: black;
}

.taskInfo {
    border: round red;
    background: #06022B;
    width: 2fr;
}

.commandPrompt {
    border: round;
    height: 3;
}

.hidden {
    display: none;
}

.title {
    border: round $accent;
}

.footer {
    height: 3;
    border: round;
}

.header {
    height: 3;
    border: round;
}

"""