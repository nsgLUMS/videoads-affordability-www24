const sleep = function (ms) {
  return new Promise((r) => {
    setTimeout(r, ms);
  });
};

const waitForVideo = async function () {
  let video = document.querySelector("video");
  while (!video) {
    console.log("waiting for video");
    await sleep(200);
    video = document.querySelector("video");
  }
};

const setQuality = async function (quality) {
  await waitForVideo();
  await sleep(1000);

  let settings = document.querySelector(
    "#header-bar > header > div > button.yt-spec-button-shape-next.yt-spec-button-shape-next--text.yt-spec-button-shape-next--overlay.yt-spec-button-shape-next--size-l.yt-spec-button-shape-next--icon-button"
  );
  settings.click();
  await sleep(500);

  let playbackSettings = document.querySelector(
    "#content-wrapper > div > div > div > ytm-menu-item:nth-child(3) > button"
  );
  playbackSettings.click();
  await sleep(500);

  let a = document.querySelector(".player-quality-settings .select").childNodes;

  let size = document.querySelector(
    ".player-quality-settings .select"
  ).childElementCount;
  if (size <= 0) {
    return "exit";
  }
  let resolutions = {};
  for (let i = 0; i < size; i++) {
    let { value } = document.querySelector(".player-quality-settings .select")
      .children[i];
    let text = document.querySelector(".player-quality-settings .select")
      .children[i].innerText;
    resolutions[text] = value;
  }

  let resolution = resolutions[quality];

  a.forEach((el) => {
    if (el.value == resolution) {
      el.selected = true;
    } else {
      el.selected = false;
    }
  });

  // dispatch change event
  let event = new Event("change", { bubbles: true });
  document
    .querySelector(".player-quality-settings .select")
    .dispatchEvent(event);

  let ok = document.querySelector(
    "body > div.dialog-container > dialog > div.dialog-buttons > c3-material-button > button"
  );
  ok.click();
};

setQuality("360p");