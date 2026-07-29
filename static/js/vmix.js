function update() {
    setTimeout(() => {
        fetch('/api/vmix')
            .then(response => response.json())
            .then(data => {
                part1(data);

                part2(data);
            });

        update();
    }, 1000);

}

// Change current_team_number to the team number that is currently selected
function part1(data) {
    try {

        if (!(current_team_number == data['current_team_number'])) {
            // Current Team Graphic
            current_team_number = data['current_team_number'];
            current_team_scrolling_image = document.getElementById('current_team_scrolling_image');
            current_team_object = document.getElementById('current_team_object');

            if (graphics_status['current_team'] === true) {
                current_team_HideTeam();

                setTimeout(async () => {
                    const response = await fetch(`/static/images/current_team/${current_team_number}.png`);
                    if (response.ok) { // response.status === 200
                        if (current_team_scrolling_image.src != `/static/images/current_team/${current_team_number}.png`) {
                            current_team_scrolling_image.src = `/static/images/current_team/${current_team_number}.png`;
                        }
                        current_team_ShowTeam();
                    }
                }, 1900);

            }
            else {
                if (current_team_scrolling_image.src != `/static/images/current_team/${current_team_number}.png`) {
                    current_team_scrolling_image.src = `/static/images/current_team/${current_team_number}.png`;
                }
            }
        }
    }
    catch (error) { }

    try {

        if (!(current_location == data['location_text'])) {
            current_location = data['location_text'];
            current_location_object = document.getElementById('location_object');

            if (graphics_status['location'] === true) {
                location_hide();

                setTimeout(() => {
                    if (current_location_object.children[1].innerHTML != current_location) {
                        current_location_object.children[1].innerHTML = current_location;
                    }
                    location_show();
                }, 1900);
            }
            else if (current_location_object.children[1].innerHTML != current_location) {
                current_location_object.children[1].innerHTML = current_location;
            }
        }
    }
    catch (error) { }

    try {

        if (JSON.stringify(current_speaker1) !== JSON.stringify(data['current_speaker1'])) {
            current_speaker1 = data['current_speaker1'];
            speaker_info_object1 = document.getElementById('speaker_info_object1');
            speaker_infoName1 = document.getElementById('speaker_infoName1');
            speaker_infoTitle1 = document.getElementById('speaker_infoTitle1');

            if (graphics_status['speaker_info1'] === true) {
                speaker_info_hide('1');

                setTimeout(() => {
                    if (current_speaker1['name'].split(' ').length > 1) {
                        speaker_infoName1.children[0].innerHTML = current_speaker1['name'].split(' ')[0];
                        speaker_infoName1.children[1].innerHTML = current_speaker1['name'].split(' ')[1];
                    }
                    else {
                        speaker_infoName1.children[0].innerHTML = current_speaker1['name'];
                        speaker_infoName1.children[1].innerHTML = '';
                    }
                    speaker_infoTitle1.innerHTML = current_speaker1['info'] || 'Speaker';

                    speaker_info_show('1');
                }, 1900);
            } else {
                speaker_info_show('1');
            }
        }
    }
    catch (error) { }

    try {
        if (JSON.stringify(current_speaker2) != JSON.stringify(data['current_speaker2'])) {
            current_speaker2 = data['current_speaker2'];
            speaker_info_object2 = document.getElementById('speaker_info_object2');
            speaker_infoName2 = document.getElementById('speaker_infoName2');
            speaker_infoTitle2 = document.getElementById('speaker_infoTitle2');

            if (graphics_status['speaker_info2'] === true) {
                speaker_info_hide('2');

                setTimeout(() => {
                    if (current_speaker2['name'].split(' ').length > 1) {
                        speaker_infoName2.children[0].innerHTML = current_speaker2['name'].split(' ')[0];
                        speaker_infoName2.children[1].innerHTML = current_speaker2['name'].split(' ')[1];
                    }
                    else {
                        speaker_infoName2.children[0].innerHTML = current_speaker2['name'];
                        speaker_infoName2.children[1].innerHTML = '';
                    }
                    speaker_infoTitle2.innerHTML = current_speaker2['info'] || 'Speaker';

                    speaker_info_show('2');
                }, 1900);
            } else {
                speaker_info_show('2');
            }
        }
    }
    catch (error) { }

    // Update last run times
    try {
        for (let i = 0; i < 3; i++) {
            if (JSON.stringify(last_run[i]) !== JSON.stringify(data['last_run'][i])) {
                if (last_run[i].show != data['last_run'][i].show) {
                    if (data['last_run'][i].show) {
                        show_last_run_times(i);
                    }
                    else {
                        hide_last_run_times(i);
                    }
                }

                last_run_number = document.getElementById(`last_run_times_car_number_container_${i}_`);
                last_run_times_best_time_result_ = document.getElementById(`last_run_times_best_time_result_${i}`);
                last_run_times_difference_result_ = document.getElementById(`last_run_times_difference_result_${i}`);
                last_run_times_university = document.getElementById(`last_run_times_university_${i}`);
                last_run_times_team_logo = document.getElementById(`last_run_times_team_logo_${i}`);
                last_run_times_car_category = document.getElementById(`last_run_times_car_category_${i}`);

                last_run_number.innerHTML = data['last_run'][i].number;
                last_run_times_best_time_result_.innerHTML = data['last_run'][i].time;
                last_run_times_difference_result_.innerHTML = data['last_run'][i].diff;
                last_run_times_university.innerHTML = teams_data[data['last_run'][i].number][4] || '';
                last_run_times_team_logo.src = `/static/icons/team_parts/${data['last_run'][i].number}.png`;

                if (teams_data[data['last_run'][i].number][8] == 'ELECTRIC') {
                    category = 'ev';
                } else {
                    category = 'cv';
                }
                last_run_times_car_category.src = `/static/icons/${category}.png`;
                console.log(`last_run_times_car_category_${i} src:`, last_run_times_car_category.src);

                last_run[i] = data['last_run'][i];
            }
        }
    }
    catch (error) { }
}

// Hide or show the team graphic
function part2(data) {
    current_team_object = document.getElementById('current_team_object');
    location_object = document.getElementById('location_object');

    if (!(data['graphics_status']['current_team'] == graphics_status['current_team'])) {
        graphics_status['current_team'] = data['graphics_status']['current_team'];

        if (data['graphics_status']['current_team']) {
            current_team_object.style.display = 'flex';
            current_team_ShowTeam();
        } else {
            current_team_HideTeam();

            setTimeout(() => {
                current_team_object.style.display = 'none';
            }, 1900);
        }
    }

    if (!(data['graphics_status']['location'] == graphics_status['location'])) {
        graphics_status['location'] = data['graphics_status']['location'];

        if (data['graphics_status']['location']) {
            location_object.style.display = 'flex';
            location_show();
        } else {
            location_hide();

            setTimeout(() => {
                location_object.style.display = 'none';
            }, 1900);
        }
    }

    if (data.graphics_status.speaker_info1 !== graphics_status.speaker_info1) {
        speaker_info_object1 = document.getElementById('speaker_info_object1');
        graphics_status.speaker_info1 = data.graphics_status.speaker_info1;

        if (data.graphics_status.speaker_info1) {
            speaker_info_object1.style.display = 'flex';
            speaker_info_show('1');
        } else {
            speaker_info_hide('1');

            setTimeout(() => {
                speaker_info_object1.style.display = 'none';
            }, 1900);
        }
    }

    if (data.graphics_status.speaker_info2 !== graphics_status.speaker_info2) {
        speaker_info_object2 = document.getElementById('speaker_info_object2');
        graphics_status.speaker_info2 = data.graphics_status.speaker_info2;

        if (data.graphics_status.speaker_info2) {
            speaker_info_object2.style.display = 'flex';
            speaker_info_show('2');
        } else {
            speaker_info_hide('2');

            setTimeout(() => {
                speaker_info_object2.style.display = 'none';
            }, 1900);
        }
    }

    if (data.graphics_status.best_time_object_ev !== graphics_status.best_time_object_ev) {
        graphics_status.best_time_object_ev = data.graphics_status.best_time_object_ev;
        best_time_object_ev = document.getElementById('best_time_object_ev');

        if (data.graphics_status.best_time_object_ev) {
            best_time_object_ev.style.display = 'flex';
            showBestTeam('ev');
        } else {
            hideBestTeam('ev');
        }
    }

    if (data.graphics_status.best_time_object_cv !== graphics_status.best_time_object_cv) {
        graphics_status.best_time_object_cv = data.graphics_status.best_time_object_cv;
        best_time_object_cv = document.getElementById('best_time_object_cv');

        if (data.graphics_status.best_time_object_cv) {
            best_time_object_cv.style.display = 'flex';
            showBestTeam('cv');
        } else {
            hideBestTeam('cv');
        }
    }
}

update();