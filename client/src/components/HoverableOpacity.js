import React, { Component } from 'react'
import { TouchableOpacity } from 'react-native'
import PropTypes from 'prop-types';

export default class HoverableOpacity extends Component {
    constructor(props) {
        super(props)
        this.state = {}
    }

    render() {
        const { outerStyle, hoverStyle } = this.props

        return (
            <TouchableOpacity
                activeOpacity={1}
                style={[{ cursor: 'inherit' }, outerStyle, this.state.hover ? hoverStyle : {}]}
                onMouseEnter={() => this.setState({ hover: true })}
                onMouseLeave={() => this.setState({ hover: false })}
            >
                <TouchableOpacity {...this.props} />
            </TouchableOpacity>
        )
    }
}

HoverableOpacity.propTypes = {
    hoverStyle: PropTypes.shape({}),
    outerStyle: PropTypes.shape({}),
}