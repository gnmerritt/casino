import $ from 'jquery';

const makeBot = () => {
  const name = $('#botName').val();
  if (!name) return;
  $.ajax({
    url: `/api/bot/${encodeURIComponent(name)}`,
    type: 'POST',
  }).done(() => {
    window.location.reload();
  });
};

export default makeBot;
