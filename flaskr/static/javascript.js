//enable popovers
const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

//enable tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

$(document).ready(async () => {
  gpus_info_interval = setIntervalImmediately(load_gpus_info, 5000);
});


function load_gpus_info() {
  $(".node-card").each((index, node) => {
    host = $(node).data().hostname;
    fetch(`/slurm/api/v1/nodes/${host}/gpus`)
      .then((response) => response.json())
      .then((json) => {
        $(node)
          .find(".gpu-card")
          .each((index, gpu) => {
            temp = json[index].temperature;
            mem_occ = (json[index].memory_occupied / 1000).toFixed(1);
            mem_tot = (json[index].type[1] / 1000).toFixed(1);
            util = json[index].gpu_utilization;
            temp_label = temperature_to_label(temp);
            $(gpu).children(".card-footer").html(`
                <span class="badge bg-${temp_label}">temp: ${temp}°</span>
                <span class="badge bg-info">mem: ${mem_occ}G / ${mem_tot}G</span>
                <span class="badge bg-secondary">usage: ${util}%</span>`);
          });
      })
      .catch((err) => console.log("Request Failed", err));
  });
}

function temperature_to_label(temp) {
  if (temp > 85) {
    return "danger";
  } else if (temp > 75) {
    return "warning";
  } else {
    return "primary";
  }
}

function setIntervalImmediately(func, interval) {
  /**
   * Immediatley execute a function and then executes it after a specific interval
   *
   * returns: The interval object
   */
  func();
  return setInterval(func, interval);
}
