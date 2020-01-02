function main(splash, args)
  splash:set_user_agent(
    "Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.93 Mobile Safari/537.36"
  )

  assert(splash:go("http://happymail.co.jp/sp/loginform.php"))
  assert(splash:wait(0.5))

  splash:evaljs("document.querySelector('input[name=TelNo]').value = 'happymail_tel_no'")
  splash:evaljs("document.querySelector('input[name=Pass]').value = 'happymail_password'")
  splash:evaljs("document.querySelector('a#login_btn').click()")
  assert(splash:wait(3))

  -- area.phpに移動
  splash:evaljs("document.querySelector('.ds_user_display_prefecture.ds_next_arrow>a').click()")
  assert(splash:wait(5))

  if splash.args.area == "東京都" then
    -- 東京都を選択
    splash:evaljs("document.querySelector('input#area-14-temporary').click()")
  else
    -- 神奈川県を選択
    splash:evaljs("document.querySelector('input#area-13-temporary').click()")
  end
  splash:evaljs("document.querySelector('button.ds_round_btn_shadow_blue').click()")
  assert(splash:wait(3))

  return splash:html()
end
