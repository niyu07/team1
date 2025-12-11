import { useEffect, useState } from "react";
import "./SearchBar.css";

interface Item {
  product: string;
  date: string;
  detail: string;
  tag: string;
  status: string;
}

export default function ShoppingList() {
  const [data, setData] = useState<Item[]>([]);
  const [query, setQuery] = useState("");
  const [field, setField] = useState("all");
  const [filtered, setFiltered] = useState<Item[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/ItemList/getItem/")
      .then((res) => res.json())
      .then((json) => {
        setData(json);
        setFiltered(json);
      })
      .catch(() => {
        setFiltered([]);
      });
  }, []);

  useEffect(() => {
    const result = data.filter((item) => matches(item, query, field));
    setFiltered(result);
  }, [query, field, data]);

  const matches = (item: Item, q: string, field: string) => {
    if (!q) return true;
    if (field === "all") {
      return Object.values(item).some((v) => String(v).includes(q));
    }
    return String(item[field as keyof Item] || "").includes(q);
  };

  return (
    <div className="container">
      <h1>買い物リスト検索</h1>

      <div className="controls">
        <input
          type="search"
          placeholder="検索ワードを入力（例：鶏、2025-01-18、朝食）"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <select value={field} onChange={(e) => setField(e.target.value)}>
          <option value="all">全項目</option>
          <option value="product">商品</option>
          <option value="date">日付</option>
          <option value="detail">詳細</option>
          <option value="tag">タグ</option>
          <option value="status">状態</option>
        </select>
        <button
          onClick={() => {
            setQuery("");
            setField("all");
          }}
        >
          クリア
        </button>
      </div>

      <div className="meta">{filtered.length} 件表示中</div>

      {filtered.length === 0 ? (
        <div className="no-result">該当するデータがありません</div>
      ) : (
        <table>
          <thead>
            <tr>
              <th>商品</th>
              <th>日付</th>
              <th>詳細</th>
              <th>タグ</th>
              <th>状態</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((item, idx) => (
              <tr key={idx} className={`status-${item.status}`}>
                <td>{item.product}</td>
                <td>{item.date}</td>
                <td>{item.detail}</td>
                <td>{item.tag}</td>
                <td>{item.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
