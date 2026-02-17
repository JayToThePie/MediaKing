import './FolderPicker.css'

function FolderPicker({ onSelect, folder, loading }) {
  return (
    <div className="folder-picker">
      <button 
        className="folder-btn" 
        onClick={onSelect}
        disabled={loading}
      >
        <span className="folder-icon">📂</span>
        {loading ? 'Loading...' : 'Select Folder'}
      </button>
      {folder && (
        <span className="folder-path" title={folder}>
          {folder.length > 50 ? '...' + folder.slice(-47) : folder}
        </span>
      )}
    </div>
  )
}

export default FolderPicker
