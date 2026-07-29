for (let i = 0; i < 3; i++) {
    if (data['last_run'][i] !== last_run[i]) {
        last_run[i] = data['last_run'][i];

        if (last_run[i].number == '0') {
            hide_last_run_times(i);
        }
        else {
            // If the number is different hide all the object
            if (last_run[i].number != data['last_run'][i].number) {
                hide_last_run_times(i);
                setTimeout(() => {
                    last_run_times_best_time_result = document.getElementById(`last_run_times_best_time_result_${i}`);
                    // Check this part
                }, 600);
            }
        }
    }
}