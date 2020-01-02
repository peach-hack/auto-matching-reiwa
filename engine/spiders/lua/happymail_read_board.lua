function try(tryFun)
  local suc, err = pcall(tryFun)
  return {
    catch = function(catchFun)
      if not suc then
        catchFun(err)
      end
    end
  }
end

function main(splash, args)
  splash:set_user_agent(
    "Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.93 Mobile Safari/537.36"
  )

  assert(splash:go("https://happymail.co.jp/sp/loginform.php"))
  assert(splash:wait(0.5))

  splash:evaljs("document.querySelector('input[name=TelNo]').value = 'happymail_tel_no'")
  splash:evaljs("document.querySelector('input[name=Pass]').value = 'happymail_password'")
  splash:evaljs("document.querySelector('a#login_btn').click()")
  assert(splash:wait(3))

  splash:evaljs("document.querySelectorAll('a.nav')[2].click()")
  assert(splash:wait(5))

  -- その他掲示板を選択
  splash:evaljs("document.querySelectorAll('li.ds_link_tab_item_bill')[1].click()")
  -- すぐ会いたいを選択
  -- splash:evaljs("document.querySelector('.billboard-genre-tab-203').click()")

  assert(splash:wait(2))

  -- load more
  for i = 1, 35 do
    try(
      function()
        splash:evaljs("document.querySelector('.list_load').click()")
        assert(splash:wait(2))
      end
    ).catch(
      function(e)
        return splash:html()
      end
    )
  end

  -- 日付操作はLuaでは面倒そうなので、とりあえず決め打ちループで。
  -- local datetime = splash:evaljs("document.querySelector('.ds_post_date').innerText")

  return splash:html()
end
