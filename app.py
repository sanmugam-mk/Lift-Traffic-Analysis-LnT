import streamlit as st
import math

# PAGE CONFIG

st.set_page_config(
    page_title="Lift Traffic Analysis",
    page_icon="🏢",
    layout="wide"
)

# CALCULATION FUNCTIONS

def average_highest_reversal_floor(N, avg_passenger_carried):

    tot_sum = 0

    for i in range(1, N):
        tot_sum += i ** avg_passenger_carried

    return N - (tot_sum / (N ** avg_passenger_carried))


def calculate_lift_traffic(
    N,
    m,
    total_people,
    absentee_percentage,
    no_lifts,
    lift_capacity,
    lift_speed,
    lift_capacity_demand,
    acc,
    to,
    tc,
    tp
):

    absentee_value = absentee_percentage / 100

    population_with_absentees = math.ceil(
        total_people * (1 - absentee_value)
    )

    avg_passenger_carried = (
        lift_capacity_demand / 100
    ) * lift_capacity

    reversal_floor = average_highest_reversal_floor(
        N,
        avg_passenger_carried
    )

    tf = 2 * math.sqrt(m / acc)

    tv = m / lift_speed

    total_time = tf + to + tc

    P = 0.8 * lift_capacity

    S = N * (1 - (1 - (1 / N)) ** P)

    RTT = (
        2 * reversal_floor * tv
        + (S + 1) * (total_time - tv)
        + 2 * P * tp
    )

    interval = RTT / no_lifts

    avg_waiting_time = (
        0.4
        + ((((1.8 * P) / lift_capacity) - 0.77) ** 2)
    ) * interval

    handling_capacity = (
        300
        * avg_passenger_carried
        * 100
    ) / (interval * population_with_absentees)

    return {
        "population_with_absentees": population_with_absentees,
        "avg_passenger_carried": avg_passenger_carried,
        "reversal_floor": reversal_floor,
        "flight_time": tf,
        "transit_time": tv,
        "total_time": total_time,
        "avg_waiting_time": avg_waiting_time,
        "handling_capacity": handling_capacity
    }

# HEADER

st.title("🏢 Lift Traffic Analysis Tool")

st.caption(
    "Automated lift traffic analysis calculator "
    "developed using Python and Streamlit"
)

st.divider()


# SIDEBAR INPUTS

st.sidebar.header("Input Parameters")


N = st.sidebar.number_input(
    "Number of Floors",
    min_value=1,
    max_value=200,
    value=45,
    step=1
)

m = st.sidebar.number_input(
    "Floor-to-floor Height (m)",
    min_value=0.1,
    value=3.35,
    step=0.1
)

total_people = st.sidebar.number_input(
    "Total Population",
    min_value=1,
    value=744,
    step=1
)

absentee_percentage = st.sidebar.number_input(
    "Absentee Percentage (%)",
    min_value=0.0,
    max_value=100.0,
    value=30.0,
    step=1.0
)

no_lifts = st.sidebar.number_input(
    "Number of Lifts",
    min_value=1,
    value=4,
    step=1
)

lift_capacity = st.sidebar.number_input(
    "Lift Capacity",
    min_value=1,
    value=10,
    step=1
)

lift_speed = st.sidebar.number_input(
    "Lift Speed (m/s)",
    min_value=0.1,
    value=4.0,
    step=0.1
)

lift_capacity_demand = st.sidebar.number_input(
    "Lift Capacity Demand (%)",
    min_value=1.0,
    max_value=100.0,
    value=80.0,
    step=1.0
)

acc = st.sidebar.number_input(
    "Acceleration (m/s²)",
    min_value=0.1,
    value=1.0,
    step=0.1
)

to = st.sidebar.number_input(
    "Door Opening Time (s)",
    min_value=0.1,
    value=1.8,
    step=0.1
)

tc = st.sidebar.number_input(
    "Door Closing Time (s)",
    min_value=0.1,
    value=2.9,
    step=0.1
)

tp = st.sidebar.number_input(
    "Passenger Transfer Time (s)",
    min_value=0.1,
    value=1.2,
    step=0.1
)


# CALCULATE BUTTON

calculate_button = st.sidebar.button(
    "Calculate",
    use_container_width=True
)


# FORMULAS SECTION

with st.expander("📘 View Key Formulas Used"):

    st.markdown("""

### 1. Average Passengers Carried
(Lift Capacity Demand / 100) × Lift Capacity

---

### 2. Average Highest Reversal Floor
N - (Σ(i^Average Passengers Carried) / N^Average Passengers Carried)

---

### 3. Flight Time per Floor
2 x √(Floor Height / Acceleration)

---

### 4. Transit Time per Floor
Floor Height / Lift Speed

---

### 5. Total Single-Floor Time
Flight Time + Door Opening Time + Door Closing Time

---

### 6. Average Waiting Time
(0.4 + ((1.8 x Effective Passengers / Lift Capacity - 0.77)²)) x Interval

Effective Passengers = 0.8 x Lift Capacity

---

### 7. Handling Capacity
(300 x Average Passengers Carried x 100)
÷
(Interval x Population with Absentees)

""")

# RESULTS SECTION

if calculate_button:

    try:

        results = calculate_lift_traffic(
            N,
            m,
            total_people,
            absentee_percentage,
            no_lifts,
            lift_capacity,
            lift_speed,
            lift_capacity_demand,
            acc,
            to,
            tc,
            tp
        )

        st.success("Calculation Completed Successfully")

        # TOP METRICS

        metric1, metric2, metric3 = st.columns(3)

        with metric1:
            st.metric(
                "Population with Absentees",
                results["population_with_absentees"]
            )

        with metric2:
            st.metric(
                "Average Waiting Time",
                f"{results['avg_waiting_time']:.1f} sec"
            )

        with metric3:
            st.metric(
                "Handling Capacity",
                f"{results['handling_capacity']:.1f}"
            )


        st.divider()


        # DETAILED RESULTS

        st.subheader("Detailed Results")


        col1, col2 = st.columns(2)


        with col1:

            st.info(
                f"Average Passengers Carried = "
                f"{results['avg_passenger_carried']:.2f}"
            )

            st.info(
                f"Average Highest Reversal Floor = "
                f"{results['reversal_floor']:.2f}"
            )

            st.info(
                f"Flight Time per Floor (tf) = "
                f"{results['flight_time']:.2f}"
            )

            st.info(
                f"Transit Time per Floor (tv) = "
                f"{results['transit_time']:.2f}"
            )


        with col2:

            st.info(
                f"Total Single-Floor Time = "
                f"{results['total_time']:.2f}"
            )

            st.warning(
                f"Average Waiting Time = "
                f"{results['avg_waiting_time']:.1f} sec"
            )

            st.success(
                f"Handling Capacity = "
                f"{results['handling_capacity']:.1f}"
            )


    except Exception as e:

        st.error(f"Error occurred: {e}")