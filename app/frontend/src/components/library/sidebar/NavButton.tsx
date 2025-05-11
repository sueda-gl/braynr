import React from 'react';

export interface NavButtonProps {
  label: string;
  count?: number;
  isActive: boolean;
  onClick: () => void;
  subItems?: { label: string; color?: string }[];
}

export const NavButton: React.FC<NavButtonProps> = (props) => {
  return (
    <div
      className={`nav-button ${props.isActive ? 'active' : ''}`}
      onClick={props.onClick}
    >
      <div className="nav-button-main">
        <span>{props.label}</span>
        <span className="nav-count">{props.count?.toString() || '0'}</span>
      </div>
      {props.subItems &&
        props.subItems.map((item, index) => (
          <div key={index} className="nav-sub-item">
            {item.color && (
              <span
                className="status-dot"
                style={{ backgroundColor: item.color }}
              ></span>
            )}
            <span>{item.label}</span>
            <span>0</span> {/* Assuming sub-item counts are static or need to be passed if dynamic */}
          </div>
        ))}
    </div>
  );
}; 