// Action types
const CREATE_COMMENT = 'CREATE_COMMENT';
const LIST_COMMENTS = 'LIST_COMMENTS';
const DELETE_COMMENT = 'DELETE_COMMENT';
const MODIFY_COMMENT = 'MODIFY_COMMENT';

// Action creators
const createComment = comment => ({ type: CREATE_COMMENT, comment });
const listComments = comments => ({ type: LIST_COMMENTS, comments });
const deleteComment = id => ({ type: DELETE_COMMENT, id });
const modifyComment = (id, comment) => ({ type: MODIFY_COMMENT, id, comment });

// Reducer
const initialState = {
  comments: [],
};

const commentsReducer = (state = initialState, action) => {
  switch (action.type) {
    case CREATE_COMMENT:
      return {
        ...state,
        comments: [...state.comments, action.comment],
      };
    case LIST_COMMENTS:
      return {
        ...state,
        comments: action.comments,
      };
    case DELETE_COMMENT:
      return {
        ...state,
        comments: state.comments.filter(comment => comment.id !== action.id),
      };
    case MODIFY_COMMENT:
      return {
        ...state,
        comments: state.comments.map(comment => {
          if (comment.id === action.id) {
            return {
              ...comment,
              ...action.comment,
            };
          }
          return comment;
        }),
      };
    default:
      return state;
  }
};

// Component
function Comments({ comments, createComment, deleteComment, modifyComment }) {
  const [newComment, setNewComment] = useState('');
  const [selectedComment, setSelectedComment] = useState(null);

  const handleCreateComment = () => {
    createComment({ id: Date.now(), text: newComment });
    setNewComment('');
  };

  const handleDeleteComment = id => {
    deleteComment(id);
  };

  const handleModifyComment = (id, comment) => {
    modifyComment(id, { text: comment });
    setSelectedComment(null);
  };

  return (
    <div>
      <h2>Comments</h2>
      <textarea value={newComment} onChange={e => setNewComment(e.target.value)} />
      <button onClick={handleCreateComment}>Create Comment</button>
      {comments.map(comment => (
        <div key={comment.id}>
          <p>{comment.text}</p>
          <button onClick={() => setSelectedComment(comment)}>Modify</button>
          <button onClick={() => handleDeleteComment(comment.id)}>Delete</button>
        </div>
      ))}
      {selectedComment && (
        <ModifyComment
          comment={selectedComment.text}
          onSave={comment => handleModifyComment(selectedComment.id, comment)}
