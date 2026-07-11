import { useState } from "react";
import { Pencil, Check, X } from "lucide-react";

interface EditableTextProps {
  value: string;
  onSave: (newValue: string) => Promise<void>;
}

export default function EditableText({ value, onSave }: EditableTextProps) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(value);
  const [saving, setSaving] = useState(false);

  async function handleSave() {
    if (!draft.trim()) return;
    setSaving(true);
    try {
      await onSave(draft);
      setEditing(false);
    } finally {
      setSaving(false);
    }
  }

  function handleCancel() {
    setDraft(value);
    setEditing(false);
  }

  if (!editing) {
    return (
      <div className="group/edit relative">
        <p className="leading-relaxed text-[15px] pr-6">{value}</p>
        <button
          onClick={() => {
            setDraft(value);
            setEditing(true);
          }}
          className="absolute top-0 right-0 opacity-0 group-hover/edit:opacity-100 text-ink-light/30 dark:text-ink-dark/30 hover:text-accent transition-all"
          aria-label="Edit"
        >
          <Pencil size={13} />
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      <textarea
        value={draft}
        onChange={(e) => setDraft(e.target.value)}
        rows={Math.max(6, draft.split("\n").length + 2)}
        autoFocus
        className="w-full bg-canvas-light dark:bg-canvas-dark border border-accent/40 rounded-lg p-3 text-[15px] leading-relaxed outline-none focus:border-accent transition-colors resize-y min-h-[150px]"
      />
      <div className="flex items-center gap-3">
        <button
          onClick={handleSave}
          disabled={saving}
          className="flex items-center gap-1 text-xs text-accent hover:text-accent-light disabled:opacity-40 transition-colors"
        >
          <Check size={13} />
          {saving ? "Saving…" : "Save"}
        </button>
        <button
          onClick={handleCancel}
          disabled={saving}
          className="flex items-center gap-1 text-xs text-ink-light/40 dark:text-ink-dark/40 hover:text-ink-light dark:hover:text-ink-dark transition-colors"
        >
          <X size={13} />
          Cancel
        </button>
      </div>
    </div>
  );
}