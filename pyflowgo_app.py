import streamlit as st
import subprocess
import sys
import tempfile
from pathlib import Path
import mpld3
import matplotlib.axis
import streamlit.components.v1 as components
import pyflowgo.run_flowgo as run_flowgo
import pyflowgo.plot_flowgo_results as plot_flowgo_results
import csv
import copy
import json
import pandas as pd


col1, col2 = st.columns([4, 1])
with col1:
    st.title("Welcome to PyFLOWGO")
with col2:
    st.image("https://github.com/pyflowgo.png",width=120)

st.markdown("This is a Web interface for [PyFLOWGO](https://github.com/pyflowgo/pyflowgo)")

# Select PyFLOWGO configuration
st.subheader("Select configuration file")

json_file = st.file_uploader("Select PyFLOWGO JSON configuration file",type=["json"])

st.subheader("Field data (optional)")

channel_width_file = st.file_uploader(
    "Channel width field data",type=["csv"],key="channel_width")

field_data_file = st.file_uploader(
    "Temperature, crystals, bubbles and viscosity field data",type=["csv"],key="field_data")

st.subheader("Effusion rate")

run_mode = st.radio(
    "Simulation mode",
    ["Single Effusion", "Effusion Rate Array"],
    horizontal=True
)

if run_mode == "Single Effusion":
    single_effusion_rate = st.number_input(
        "Single Effusion Rate",
        min_value=0.0,
        value=500.0,
        step=1.0
    )
else:
    rate_col1, rate_col2, rate_col3 = st.columns(3)

    with rate_col1:
        first_eff_rate = st.number_input(
            "First Effusion Rate",
            min_value=0,
            value=100,
            step=1
        )

    with rate_col2:
        last_eff_rate = st.number_input(
            "Last Effusion Rate",
            min_value=0,
            value=300,
            step=1
        )

    with rate_col3:
        step_eff_rate = st.number_input(
            "Step Effusion Rate",
            min_value=1,
            value=100,
            step=1
        )

st.subheader("Result folder")
results_folder_input = st.text_input("Results folder path",value="")


# Run PyFLOWGO
if st.button("▶ Run PyFLOWGO"):

    if json_file is None:
        st.warning("Please select a JSON configuration file first.")
        st.stop()

    # Save uploaded JSON to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        tmp.write(json_file.getbuffer())
        json_path = Path(tmp.name)

    json_name = Path(json_file.name).stem

    #add field data if needed
    channel_width_path = None
    field_data_path = None

    if channel_width_file is not None:
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            tmp.write(channel_width_file.getbuffer())
            channel_width_path = Path(tmp.name)

    if field_data_file is not None:
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            tmp.write(field_data_file.getbuffer())
            field_data_path = Path(tmp.name)


    # Define results folder and working directory
    if not results_folder_input:
        st.warning("Please select a results folder.")
        st.stop()

    results_folder = Path(results_folder_input).expanduser().resolve()
    results_folder.mkdir(parents=True, exist_ok=True)

    #working_dir = Path(tempfile.mkdtemp(prefix="pyflowgo_"))
    #results_link = working_dir / "results_flowgo"
    #results_link.symlink_to(results_folder, target_is_directory=True)
    working_dir = results_folder.parent

    # --------------------------------------------------
    # Build the configuration used for THIS run.
    # The uploaded JSON is never modified.
    # --------------------------------------------------
    with open(json_path, "r", encoding="utf-8") as f:
        run_config = json.load(f)

    if run_mode == "Single Effusion":
        run_config["effusion_rate_init"] = float(single_effusion_rate)
    else:
        if last_eff_rate < first_eff_rate:
            st.error("Last Effusion Rate must be greater than or equal to First Effusion Rate.")
            st.stop()

        run_config["effusion_rate_init"] = [
            int(first_eff_rate),
            int(last_eff_rate),
            int(step_eff_rate)
        ]

    # Keep this temporary JSON until plotting is complete because
    # PyFLOWGO also reads configuration values while making figures.
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        delete=False,
        encoding="utf-8"
    ) as tmp_run:
        json.dump(run_config, tmp_run, indent=4)
        run_json_path = Path(tmp_run.name)

    st.info(f"🔵 PyFLOWGO is running, please wait ...\n\nResults folder: {results_folder}")

    # Start PyFLOWGO
    process = subprocess.Popen(
        [
            sys.executable,
            "-u",
            str(Path(__file__).resolve().parent / "main_run_and_plot_flowgo.py"),
            str(run_json_path)
        ],
        cwd=str(working_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    # Display last 10 lines
    output_area = st.empty()
    last_lines = []

    for line in iter(process.stdout.readline, ""):
        line = line.rstrip()
        if line:
            last_lines.append(line)
            last_lines = last_lines[-10:]
            output_area.code("\n".join(last_lines))

    process.wait()

    # Final status
    if process.returncode == 0:
        st.success("🟢 PyFLOWGO finished successfully 🌋")
    else:
        st.error(f"🔴 PyFLOWGO failed (return code {process.returncode}).")
        st.stop()

    # Show Results
    st.subheader("Results")

    # Get PyFLOWGO result CSV files
    flowgo = run_flowgo.RunFlowgo()

    # Configuration actually used for this run
    config = run_config
    effusion_rate = config.get("effusion_rate_init")

    filename_results = []

    # --------------------------------------------------
    # Multiple effusion rates: [start, stop, step]
    # --------------------------------------------------
    if isinstance(effusion_rate, list):

        first_rate = effusion_rate[0]
        last_rate = effusion_rate[1]
        step_rate = effusion_rate[2]

        expected_rates = list(
            range(
                int(first_rate),
                int(last_rate) + 1,
                int(step_rate)
            )
        )

        # Search only PyFLOWGO result files
        for csv_file in sorted(results_folder.glob("results_flowgo_*.csv")):

            try:
                test_df = pd.read_csv(csv_file, nrows=1)

                # Must be a real PyFLOWGO result
                if "effusion_rate" not in test_df.columns:
                    continue

                # Get effusion rate stored in result
                rate = round(float(test_df.iloc[0]["effusion_rate"]))

                # Keep only requested rates
                if rate in expected_rates:
                    filename_results.append(str(csv_file))

            except Exception:
                continue

    # --------------------------------------------------
    # Single effusion rate
    # --------------------------------------------------
    else:

        filename_result = flowgo.get_file_name_results(
            str(results_folder),
            str(run_json_path)
        )

        if Path(filename_result).exists():
            filename_results.append(filename_result)

    # --------------------------------------------------
    # Check results
    # --------------------------------------------------
    if not filename_results:
        st.warning("PyFLOWGO result CSV not found.")
        st.stop()

    st.write(f"{len(filename_results)} PyFLOWGO result file(s) found:")

    for f in filename_results:
        st.write(Path(f).name)
    # Generate Matplotlib figures
    figures = plot_flowgo_results.plot_all_results(str(results_folder), filename_results, str(run_json_path))
    # Add field data to PyFLOWGO figures
    if field_data_path is not None:
        field_distance = []
        field_temp = []
        field_crystals = []
        field_bubbles = []
        field_visco_IDE = []
        field_visco_CDE = []

        with open(field_data_path) as csvf:
            csvreader = csv.DictReader(csvf, delimiter=",")
            for row in csvreader:
                field_distance.append(float(row["Distance(m)"]))
                field_temp.append(float(row["glass_temp"]))
                field_crystals.append(float(row["Xstal_fraction"]))
                field_bubbles.append(float(row["Bubble_fraction"]))
                field_visco_IDE.append(10 ** float(row["Viscosity_IDE(Pas)"]))
                field_visco_CDE.append(10 ** float(row["Viscosity_CDE(Pas)"]))

        # Temperature -> axis 0
        figures[0].axes[0].plot(field_distance, field_temp,"ro", label="Field data")
        figures[0].axes[1].plot(field_distance, field_crystals,"ro", label="Field data")
        figures[0].axes[2].plot(field_distance, field_bubbles,"ro", label="Field data")
        figures[0].axes[4].plot(field_distance, field_visco_IDE,"ro", label="Field data IDE")
        figures[0].axes[4].plot(field_distance, field_visco_CDE,"r.", label="Field data CDE")

    if channel_width_path is not None:
        field_distance_width = []
        field_width = []

        with open(channel_width_path) as csvf:
            csvreader = csv.DictReader(csvf, delimiter=",")
            for row in csvreader:
                field_distance_width.append(float(row["Distance_(m)"]))
                field_width.append(float(row["Measured_Width_(m)"]))

        figures[0].axes[6].plot(field_distance_width,field_width,"ro",label="Field data")

    # Remove legends from all axes
    for ax in figures[0].axes:
        legend = ax.get_legend()
        if legend:
            legend.remove()

    # Get legend from first axis
    handles, labels = figures[0].axes[0].get_legend_handles_labels()

    # Global legend at bottom
    figures[0].legend(
        handles,
        labels,
        loc="lower center",
        ncol=len(labels),
        frameon=False
    )

    figures[0].subplots_adjust(bottom=0.12)
    # Compatibility patch for mpld3 + Matplotlib 3.7.2
    if not hasattr(matplotlib.axis.Axis, "get_converter"):
        matplotlib.axis.Axis.get_converter = lambda self: self.converter

    figure_names = [
        "Lava properties",
        "Heat fluxes",
        "Crustal conditions",
        "Slope"
    ]

    for name, fig in zip(figure_names, figures):
        st.subheader(name)

        # Copy figure for web display
        fig_web = copy.deepcopy(fig)
        fig_web.set_size_inches(7, 7)
        # Adapt fonts and grids for web display
        for ax in fig_web.axes:
            ax.set_xlabel(ax.get_xlabel(), fontsize=7)
            ax.set_ylabel(ax.get_ylabel(), fontsize=7)
            ax.set_title(ax.get_title(), fontsize=5)
            ax.grid(False)

            legend = ax.get_legend()
            if legend is not None:
                for text in legend.get_texts():
                    text.set_fontsize(5)
                legend.get_title().set_fontsize(5)

        fig_web.tight_layout()
        html = mpld3.fig_to_html(fig_web)
        components.html(html,width=800,height=800,scrolling=True)

    # Save figures after adding field data
    if field_data_path is not None or channel_width_path is not None:
        figure_name = "lava_properties_with_field_data.png"
    else:
        figure_name = "lava_properties.png"

    figures[0].savefig(results_folder / figure_name,dpi=300,bbox_inches="tight")

    # Clean up temporary files created by the web interface
    for temporary_file in (run_json_path, json_path, channel_width_path, field_data_path):
        if temporary_file is not None:
            try:
                Path(temporary_file).unlink(missing_ok=True)
            except Exception:
                pass
