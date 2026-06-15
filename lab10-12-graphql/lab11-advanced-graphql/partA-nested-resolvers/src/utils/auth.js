const jwt = require('jsonwebtoken');
const JWT_SECRET = 'your-secret-key-change-this';

const generateToken = (user) => {
  return jwt.sign(
    { userId: user.id, role: user.role },
    JWT_SECRET,
    { expiresIn: '24h' }
  );
};

const authenticate = (context) => {
  const authHeader = context.req.headers.authorization;
  if (!authHeader) {
    throw new Error('Authentication required');
  }
  
  const token = authHeader.replace('Bearer ', '');
  try {
    return jwt.verify(token, JWT_SECRET);
  } catch (error) {
    throw new Error('Invalid token');
  }
};

const authorize = (user, requiredRole) => {
  if (user.role !== requiredRole && user.role !== 'admin') {
    throw new Error(`Insufficient permissions. Required role: ${requiredRole}`);
  }
};

module.exports = { generateToken, authenticate, authorize };
