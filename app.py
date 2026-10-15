from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

# 暫時使用 list 儲存文章，重啟程式後資料會消失
posts = [
    {
        "id": 1,
        "title": "My First Blog Post 我的第一篇文章",
        "author": "小明",
        "content": "Welcome to my blog! 歡迎來到我的部落格！\nThis is my first post. 這是我的第一篇文章。"
    },
    {
        "id": 2,
        "title": "學習 Python Flask",
        "author": "小華",
        "content": "Flask 是一個輕量級的 Python Web 框架。\n可以用來快速建立網站。"
    }
]


@app.route("/")
def index():
    """顯示所有文章"""
    return render_template("index.html", posts=posts)


@app.route("/post/<int:post_id>")
def post_detail(post_id):
    """顯示單篇文章"""
    post = next(
        (p for p in posts if p["id"] == post_id),
        None
    )

    if post is None:
        abort(404)

    return render_template("post.html", post=post)


@app.route("/new", methods=["GET", "POST"])
def new_post():
    """新增文章"""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        content = request.form.get("content", "").strip()

        # 確認三個欄位都有填寫
        if not title or not author or not content:
            return render_template(
                "new_post.html",
                error="標題、作者與文章內容都必須填寫。",
                title=title,
                author=author,
                content=content
            ), 400

        # 產生新的文章 ID
        new_id = max(
            (p["id"] for p in posts),
            default=0
        ) + 1

        post = {
            "id": new_id,
            "title": title,
            "author": author,
            "content": content
        }

        posts.append(post)

        return redirect(url_for("post_detail", post_id=new_id))

    return render_template(
        "new_post.html",
        title="",
        author="",
        content=""
    )


if __name__ == "__main__":
    app.run(debug=True)