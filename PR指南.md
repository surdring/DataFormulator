# PR（Pull Request）详细指南（适用于本仓库）

本指南面向第一次使用 GitHub 的同学，目标是让你能**安全、可审阅、可回滚**地把一个分支的改动合并进主分支（例如把 `upgrade-0.5.1` 合并到 `main`）。

---

## 1. PR 是什么？

**PR（Pull Request）= 合并请求**。

它解决的问题是：

- 你在一个分支（比如 `upgrade-0.5.1`）做了一批改动
- 你希望把这批改动合并进另一个分支（比如 `main`）
- 在合并前，你需要一个“检查窗口”：
  - 看清楚改动（diff）
  - 讨论/评论
  - 跑自动化检查（CI，如果仓库配置了）
  - 最终点按钮合并

你可以把 PR 理解为：**把“合并”变成一个可审阅的流程**，而不是直接在本地 `git merge` 然后 push。

---

## 2. 为什么建议用 PR，而不是直接在本地合并？

- **可审阅**：GitHub 会展示所有文件差异，避免“合进去才发现问题”。
- **可追溯**：PR 里有讨论和链接，事后容易复盘。
- **更安全**：合并前后都能回滚（revert merge 或回退 commit）。
- **更适合多人协作**：即便现在只有你一个人，后续有人参与也不需要改流程。

---

## 3. PR 的几个关键概念

- **base（目标分支）**：你要合并到哪里。通常是 `main`。
- **compare（来源分支）**：你的改动在哪里。比如 `upgrade-0.5.1`。
- **diff**：两个分支之间的代码差异。
- **review（审阅）**：对 diff 的检查和讨论。

---

## 4. 本仓库的典型 PR 场景（强烈推荐的工作方式）

### 场景 A：升级官方版本（本次就是这个）

目标：把升级成果合进 `main`。

- 来源分支：`upgrade-0.5.1`
- 目标分支：`main`

### 场景 B：日常开发新功能

目标：把某个功能开发完成后合并进 `main`。

- 来源分支：例如 `feat-report-style`、`fix-xxx`、`perf-xxx`
- 目标分支：`main`

---

## 5. 创建 PR：网页操作步骤（最常用）

1. 打开 GitHub 仓库页面：`https://github.com/surdring/DataFormulator`
2. 点击顶部标签：`Pull requests`
3. 点击按钮：`New pull request`
4. 选择分支：
   - **base**：`main`
   - **compare**：`upgrade-0.5.1`
5. 确认页面显示的 diff 没问题
6. 填写标题和描述（建议见下面的模板）
7. 点击：`Create pull request`

---

## 6. PR 描述模板（建议直接复制）

**标题建议**（二选一）：

- `chore: upgrade base to 0.5.1 and keep localization`
- `chore: sync upstream tag 0.5.1 + reapply Chinese localization`

**描述模板**：

```text
## 背景
- 目标：升级到官方 tag 0.5.1，同时保留本地中文化与后端改造。

## 改动摘要
- 基线：切换到官方 0.5.1
- 迁移：中文 i18n、报告生成中文 prompt、关键视图中文化
- 工程：.gitignore 增强（忽略 .env/api-keys.env/egg-info），yarn.lock 更新

## 验证
- yarn build: PASS
- python compileall: PASS
- 手工验证：启动服务后检查中文 UI / 报告生成 / 数据加载（待/已完成）

## 注意事项
- 不提交 .env / api-keys.env（使用 template 文件）
```

---

## 7. PR 审阅清单（合并前必看）

### 7.1 安全与敏感信息

- **确认没有提交**：`.env`、`api-keys.env`、任何 token/密码
- 本仓库推荐做法：
  - 提交 `*.template`（例如 `api-keys.env.template`）
  - 本地真实配置只放在 `.env` / `api-keys.env`（并在 `.gitignore` 忽略）

### 7.2 生成物/大文件

- 一般不建议提交：`*.egg-info/`、`venv/`、`node_modules/`
- `yarn.lock` **应该提交**（保证依赖可复现）

### 7.3 升级 PR 的关键文件（本仓库经验）

升级时冲突/风险更高的区域：

- 前端中文化：
  - `src/i18n/zhCN.ts`
  - `src/views/*`（尤其 Report/DataThread/Chat）
- 后端报告生成：
  - `py-src/data_formulator/agents/agent_report_gen.py`
  - `py-src/data_formulator/agent_routes.py`

审阅重点：

- 中文 `t()` 调用是否仍然正确
- 上游新增的字段/逻辑是否被你覆盖掉
- 报告生成是否仍按你定制的结构输出

---

## 8. 合并策略怎么选？（Merge / Squash / Rebase）

在 PR 页面点击 `Merge` 时，通常会有三种方式：

- **Merge commit**（推荐：默认且直观）
  - 会生成一个合并提交
  - 历史清晰，适合升级类 PR

- **Squash and merge**（推荐：历史更干净）
  - 把来源分支的多个 commit 压成一个 commit
  - 适合“分支里 commit 很碎”的情况

- **Rebase and merge**（新手不建议）
  - 历史线性，但容易在多人协作时引入理解成本

对本次升级，我建议：

- 如果你希望保留升级过程：选 **Merge commit**
- 如果你只想主分支看起来干净：选 **Squash and merge**

---

## 9. 合并后你本地该怎么同步？

合并 PR 后（`main` 被更新），你本地通常要做：

```bash
git checkout main
git pull
```

然后如果你不再需要升级分支：

```bash
git branch -d upgrade-0.5.1
```

远端分支是否删除看你习惯（一般可以删）。

---

## 10. 常见问题与排查

### 10.1 `Connection closed ... port 22`（SSH 22 被封）

现象：`git push` 失败，提示 22 端口连接被关闭。

解决：改用 HTTPS：

```bash
git remote set-url origin https://github.com/<USER>/<REPO>.git
git push
```

（你之前已经用 HTTPS 成功 push 了。）

### 10.2 `remote: Repository not found` / `无法读取远程仓库`

常见原因：

- 仓库名字写错（大小写也要一致）
- 你没有权限（private repo）
- HTTPS 方式需要 PAT（token）而不是 GitHub 登录密码

### 10.3 不小心把敏感信息提交了怎么办？

- **如果还没 push 到远端**：优先用 `git commit --amend` 或 `git reset` 清掉，再提交。
- **如果已经 push**：
  - 立即作废/更换泄露的 key
  - 视情况使用历史重写工具清理（这一步风险较高，建议先咨询/备份）

---

## 11. 后续如何持续跟官方同步（建议流程）

你现在已经配置了：

- `origin`：你自己的 GitHub 仓库
- `upstream`：官方仓库 `microsoft/data-formulator`

建议后续每次升级都走：

- 先从官方选择一个明确版本（tag）或某个提交
- 新建分支做升级
- 跑构建/启动验证
- 发 PR 合并

这样可以把“升级风险”隔离在分支里，主分支始终可用。
