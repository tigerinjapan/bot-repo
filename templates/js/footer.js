function writeFooter(userDiv) {

  if (userDiv == SYM_BLANK) {
    return;
  }

  const addr = "東京都新宿区新宿ビル5F";
  const tel = "042-1234-567";
  const mailAddr = "kobe_dev@jh.com";

  const footerContents = (`
    <div class="footer">
      <p>
        <address>${addr}</address>
        Tel : <a href="tel:">${tel}</a><br>
        E-MAIL : <a href="mailto:${mailAddr}">${mailAddr}</a><br>
        <small>COPYRIGHT@KOBE_DEV CORP. ALL RIGHTS RESERVED.</small>
      </p>
    </div>`);

  if (userDiv == AUTH_ADMIN) {
    document.getElementsByTagName("footer")[0].innerHTML = footerContents;
  }
}
